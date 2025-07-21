#include "llvm/Passes/PassPlugin.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Transforms/Utils/ModuleUtils.h"
#include "dcov_common.h"

using namespace llvm;

namespace {
    static unsigned int bb_instrumented = 0;

    struct DCovPass : public PassInfoMixin<DCovPass> {
        
        bool shouldInstrumentFunction(Function &F) {
            // Skip functions without names
            if (F.getName().empty()) return false;

            if (F.size()<1) return false;
            
            // Skip LLVM related functions
            std::string name = F.getName().str();
            
            // Skip functions with long names
            if (name.length() > 50) return false;

            // Skip special functions
            static constexpr const char *ignoreList[] = {
                "main",
                "lambda",
                "anonymous",
                "operator",
                "llvm",
                "llvh",
                "asan.",
                "llvm.",
                "sancov.",
                "__ubsan_",
                "ign.",
                "__afl_",
                "_fini",
                "__libc_csu",
                "__asan",
                "__msan",
                "__cmplog",
                "__sancov",
                "msan.",
                "LLVMFuzzerM",
                "LLVMFuzzerC",
                "LLVMFuzzerI",
                "__decide_deferred",
                "maybe_duplicate_stderr",
                "discard_output",
                "close_stdout",
                "dup_and_close_stderr",
                "maybe_close_fd_mask",
                "ExecuteFilesOnyByOne",
                "identifyCallsites",
                "getenv",
                "atoi",
                "shmget",
                "shmat",
                "__dcov_init"
            };
            
            for (auto const &ignoreFunc : ignoreList) {
                if (name.find(ignoreFunc) == 0) {
                    return false;
                }
            }
            
            return true;
        }
        
        bool shouldInstrumentBlock(BasicBlock &BB) {
            // Only instrument blocks with multiple predecessors
            unsigned numPreds = 0;
            for (auto *Pred : predecessors(&BB)) {
                numPreds++;
                if (numPreds > 1) return true;
            }
            return false;
        }
        
        unsigned int hashBB(Function &F, BasicBlock &BB) {
            // Simple hash combining function name and BB address
            std::hash<std::string> hasher;
            std::string bbID = F.getName().str() + std::to_string((uintptr_t)&BB);
            return hasher(bbID) % bitmap_size;
        }

        PreservedAnalyses run(Module& M, ModuleAnalysisManager &MAM);
        
    };
} // namespace

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
    return {
        LLVM_PLUGIN_API_VERSION, "DCovCoverage", "v1.0",
        [](PassBuilder &PB) {
            PB.registerOptimizerLastEPCallback(
                [](ModulePassManager &MPM, OptimizationLevel OL){
                    MPM.addPass(DCovPass());
                });
        }
    };
}

PreservedAnalyses DCovPass::run(Module &M, ModuleAnalysisManager &AM) {
    fprintf(stdout, "\n\033[36mIntrumenting Model: %s\033[0m\n", M.getName().str().c_str());
    LLVMContext &C = M.getContext();
    
    Type *VoidTy = Type::getVoidTy(C);
    IntegerType *Int8Ty = IntegerType::getInt8Ty(C);
    IntegerType *Int32Ty = IntegerType::getInt32Ty(C);
    PointerType *Int8PtrTy = Type::getInt8PtrTy(C);
    PointerType *VoidPtrTy = Type::getInt8PtrTy(C);

    IRBuilder<> ModBuilder(C);

    GlobalVariable *dcovMapPtr = new GlobalVariable(
        M, Int8PtrTy, false, GlobalValue::CommonLinkage, 
        ConstantPointerNull::get(Int8PtrTy), "__dcov_map_ptr"
    );
    
    // 创建初始化dcovMapPtr的函数
    FunctionType *initMemFuncTy = FunctionType::get(Type::getVoidTy(C), false);

    Function *initMemFunc = Function::Create(
        initMemFuncTy, GlobalValue::CommonLinkage, "__dcov_init", &M
    );

    BasicBlock *initMemBB = BasicBlock::Create(C, "entry", initMemFunc);
    ModBuilder.SetInsertPoint(initMemBB);

    // Get required functions
    FunctionCallee getenvFunc = M.getOrInsertFunction(
        "getenv", Int8PtrTy, Int8PtrTy);
    FunctionCallee atoiFunc = M.getOrInsertFunction(
        "atoi", Int32Ty, Int8PtrTy);
    FunctionCallee shmgetFunc = M.getOrInsertFunction(
        "shmget", Int32Ty, Int32Ty, Int32Ty, Int32Ty);
    FunctionCallee shmatFunc = M.getOrInsertFunction(
        "shmat", Int8PtrTy, Int32Ty, Int8PtrTy, Int32Ty);
    FunctionCallee printfFunc = M.getOrInsertFunction(
        "printf", 
        FunctionType::get(Int32Ty, {PointerType::get(Int8Ty, 0)}, true)
    );
    
    
    Value *envVarName = ModBuilder.CreateGlobalStringPtr("DCOV_KEY_C");
    Value *envVar = ModBuilder.CreateCall(getenvFunc, {envVarName});
    
    /* Build:
    int shmKey = 4400;
    if (envVar != NULL){
        shmKey = atoi(envVar);
    } */ 
    AllocaInst *shmKeyVar = ModBuilder.CreateAlloca(Int32Ty, nullptr, "__shmKey");
    ModBuilder.CreateStore(ConstantInt::get(Int32Ty, 4400, true), shmKeyVar);

    BasicBlock *thenBlock = BasicBlock::Create(C, "then", initMemFunc);
    BasicBlock *elseBlock = BasicBlock::Create(C, "else", initMemFunc);
    BasicBlock *endBlock = BasicBlock::Create(C, "end", initMemFunc);
    Value *cond = ModBuilder.CreateICmpNE(envVar, ConstantPointerNull::get(Int8PtrTy));
    ModBuilder.CreateCondBr(cond, thenBlock, elseBlock);
    
    // then
    ModBuilder.SetInsertPoint(thenBlock);
    Value* newShmKey = ModBuilder.CreateCall(atoiFunc, {envVar});
    ModBuilder.CreateStore(newShmKey, shmKeyVar);
    ModBuilder.CreateBr(endBlock);
    
    // else
    ModBuilder.SetInsertPoint(elseBlock);
    ModBuilder.CreateBr(endBlock);

    // end
    ModBuilder.SetInsertPoint(endBlock);
    Value *shmKey = ModBuilder.CreateLoad(Int32Ty, shmKeyVar);

    // printf("DCOV Loaded with DCOV_KEY_C=%d\n", shmKey);
    // ModBuilder.CreateCall(printfFunc, {ModBuilder.CreateGlobalStringPtr("DCOV Loaded with DCOV_KEY_C=%d\n"), shmKey});

    // shmId = shmget(shmKey, shmSize, shmFlags);
    Value *shmSize = ConstantInt::get(Int32Ty, bytemap_size);
    Value *shmFlags = ConstantInt::get(Int32Ty, 01000 | 0666);
    Value *shmId = ModBuilder.CreateCall(shmgetFunc, {shmKey, shmSize, shmFlags});

    // shmPtr = shmat(shmId, NULL, 0);
    Value *NullPtr = ConstantPointerNull::get(VoidPtrTy);
    Value *shmFlags2 = ConstantInt::get(Int32Ty, 0);
    Value *shmPtr = ModBuilder.CreateCall(shmatFunc, {shmId, NullPtr, shmFlags2});

    // dcovMapPtr = (unsigned char *)shmPtr;
    ModBuilder.CreateStore(shmPtr, dcovMapPtr);
    ModBuilder.CreateRetVoid();

    // Add constructor to call initialization
    appendToGlobalCtors(M, initMemFunc, 65535);

    GlobalVariable *DcovPrevLoc = new GlobalVariable(
        M, Int32Ty, false, GlobalValue::CommonLinkage, 
        ConstantInt::get(Int32Ty, 0), "__dcov_prev_loc"
    );

    unsigned int blocks = 0;
    for (auto &F : M) {
        if (!shouldInstrumentFunction(F)) continue;;
        
        fprintf(stdout, "  \033[32mLooking Function: %s (%zu)\033[0m\n", F.getName().str().c_str(), F.size());
        
        
        // Instrument each basic block
        for (BasicBlock &BB : F) {
            if (!shouldInstrumentBlock(BB)) continue;
            
            uint32_t bbIdx = hashBB(F, BB);
            Value *bbIdxVal = ConstantInt::get(Int32Ty, bbIdx);
            
            IRBuilder<> Builder(&BB, BB.getFirstInsertionPt());

            
            
            // Load previous location
            Value *PrevLocVal = Builder.CreateLoad(Int32Ty, DcovPrevLoc);
            
            // Calculate edge index: edge_idx = bb_idx ^ prev_loc
            Value *EdgeIdx = Builder.CreateXor(bbIdxVal, PrevLocVal);
            
            // Calculate byte offset: byte_offset = edge_idx / 8
            Value *ByteOffset = Builder.CreateLShr(EdgeIdx, ConstantInt::get(Int32Ty, 3));
            
            // Get target byte pointer: tgt_byte_ptr = shm_ptr + byte_offset
            Value *ShmPtrVal = Builder.CreateLoad(Int8PtrTy, dcovMapPtr);
            Value *TgtBytePtr = Builder.CreateGEP(Int8Ty, ShmPtrVal, ByteOffset);
            
            // Calculate bit offset: bit_offset = edge_idx % 8
            Value *BitOffset = Builder.CreateAnd(EdgeIdx, ConstantInt::get(Int32Ty, 7));
            
            // Calculate new byte: new_byte = 1 << bit_offset
            Value *NewByte = Builder.CreateShl(
                ConstantInt::get(Int8Ty, 1), 
                Builder.CreateTrunc(BitOffset, Int8Ty));
            
            // Atomic OR operation: *tgt_byte_ptr |= new_byte
            Value *OldByte = Builder.CreateAtomicRMW(
                AtomicRMWInst::Or, TgtBytePtr, NewByte,
                MaybeAlign(), AtomicOrdering::SequentiallyConsistent);
            
            // Update previous location: prev_loc = bb_idx >> 1
            Builder.CreateStore(ConstantInt::get(Int32Ty, bbIdx>>1), DcovPrevLoc);
            blocks++;
        }
    }
    bb_instrumented += blocks;   
    if (blocks){
        fprintf(stdout, "\033[36mInstrumented %d blocks\033[0m\n", blocks);
    } else {
        fprintf(stdout, "\033[36mNo blocks found\033[0m\n");
    }  
    return PreservedAnalyses();
}
