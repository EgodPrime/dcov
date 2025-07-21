#include "gcc-plugin.h"
#include "plugin-version.h"
#include <sys/shm.h>

#include "tree.h"
#include "context.h"
#include "basic-block.h"
#include "gimple-pretty-print.h"
#include "gimple.h"
#include "gimple-iterator.h"
#include "tree-ssa-alias.h"
#include "tree-pass.h"
#include "function.h"
#include "coretypes.h"
#include "basic-block.h"
#include "stringpool.h"
#include "cgraph.h"
#include "gimplify.h"
#include <context.h>
#include "memmodel.h"

#include <iostream>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <tree-iterator.h>
#include <c-family/c-common.h>
#include <c-tree.h>
#include <print-tree.h>

static uint32_t bitmap_size = 1<<20;

inline uint32_t rotl32 ( uint32_t x, int8_t r ){
    return (x << r) | (x >> (32 - r));
}

#define	ROTL32(x,y)	rotl32(x,y)

inline uint32_t fmix32 ( uint32_t h ){
    h ^= h >> 16;
    h *= 0x85ebca6b;
    h ^= h >> 13;
    h *= 0xc2b2ae35;
    h ^= h >> 16;

    return h;
}

uint32_t MurmurHash3_x86_32 (const void * key, int len, uint32_t seed){
    const uint8_t * data = (const uint8_t*)key;
    const int nblocks = len / 4;

    uint32_t h1 = seed;

    const uint32_t c1 = 0xcc9e2d51;
    const uint32_t c2 = 0x1b873593;

    const uint32_t * blocks = (const uint32_t *)(data + nblocks*4);

    for(int i = -nblocks; i; i++)
    {
        uint32_t k1 = blocks[i];

        k1 *= c1;
        k1 = ROTL32(k1,15);
        k1 *= c2;

        h1 ^= k1;
        h1 = ROTL32(h1,13); 
        h1 = h1*5+0xe6546b64;
    }

    const uint8_t * tail = (const uint8_t*)(data + nblocks*4);

    uint32_t k1 = 0;

    switch(len & 3){
        case 3: k1 ^= tail[2] << 16;
        case 2: k1 ^= tail[1] << 8;
        case 1: k1 ^= tail[0];
        k1 *= c1; k1 = ROTL32(k1,15); k1 *= c2; h1 ^= k1;
    };

    h1 ^= len;

    h1 = fmix32(h1);

    return h1;
} 

uint32_t hash_bb(function*fun, basic_block bb){
    char str[256] {'\0'};
    strcat(str, function_name(fun));
    char bb_idx_str[16] = {0};
    sprintf(bb_idx_str, "%d",bb->index);
    strcat(str, bb_idx_str);
    uint32_t hash = MurmurHash3_x86_32(str, strlen(str), 0);
    return hash % bitmap_size;
}

int plugin_is_GPL_compatible = 1;

namespace{
    static struct plugin_info dcov_plugin_info = {
        .version = "1.0",
        .help = "Track every edge execution",
    };
    
    const pass_data dcov_ins_pass_data = 
    {
        .type = GIMPLE_PASS,
        .name = "dcov",        
        .optinfo_flags = OPTGROUP_NONE,        
        .tv_id = TV_NONE,
        .properties_required = 0,
        .properties_provided = 0,
        .properties_destroyed = 0,
        .todo_flags_start = 0,
        .todo_flags_finish = (TODO_update_ssa | TODO_cleanup_cfg | TODO_verify_il),
    };

    unsigned int bb_instrumented = 0;

    struct dcov_pass : gimple_opt_pass
    {
        dcov_pass(gcc::context *ctx)
            : gimple_opt_pass(dcov_ins_pass_data, ctx)
        {}

        virtual unsigned int execute(function *fun) override
        {      
            if(!fun) return 0;

            if (!should_instrument_function(fun)) return 0;

            const char* file_name = LOCATION_FILE(fun->function_start_locus);

            // skip unkown files
            if(!file_name) return 0;
            // 如果文件名包含llvm或者llvh，则跳过
            if(strstr(file_name, "llvm")!=NULL || strstr(file_name, "llvh") || strstr(file_name, "Optimizer")!=NULL) return 0;
            // skip headers
            if(strstr(file_name, ".h")!=NULL) return 0;

            const char* fun_name = function_name(fun);
            // skip name too long
            if(strlen(fun_name)>50) return 0;
            // skip lambda
            if(!strcmp(IDENTIFIER_POINTER(DECL_NAME(fun->decl)),"<lambda>")) return 0;
            if(strstr(fun_name, "anonymous")!=NULL) return 0;
            if(strstr(fun_name, "operator")!=NULL) return 0;
            // skil main
            if(!strcmp(fun_name,"main"))  return 0;

            std::cerr << "\033[36m[ENTRY] "
                    << function_name(fun) << " at "
                    << (LOCATION_FILE(fun->function_start_locus) ? : "<unknown>") << ":" << LOCATION_LINE(fun->function_start_locus)<<"\n";
            std::cerr<<"\033[0m";

            int blocks = 0;

            // types can beused
            tree void_ptr_type = build_pointer_type(void_type_node);
            tree uint8_ptr_type = build_pointer_type(uint8_type_node);
            tree char_ptr_type = build_pointer_type(char_type_node);
            tree const_char_ptr_type = build_qualified_type(char_ptr_type, TYPE_QUAL_CONST);

            /* These are temporaries used by inline instrumentation only, that
            are live throughout the function.  */
            tree ploc = NULL, gploc=create_tmp_var(uint32_type_node, ".gploc"), edge_idx = NULL, byte_offset=NULL, bit_offset=NULL, new_byte=NULL, 
                dcov_mdata_ptr = NULL, tgt_byte_ptr = NULL;

            basic_block bb;
            FOR_ALL_BB_FN(bb, fun){   
                if (!should_instrument_block(bb)) continue;
                uint32_t bb_idx_i = hash_bb(fun, bb);
                tree bb_idx = build_int_cst(uint32_type_node, bb_idx_i);
            
                /*
                uint32_t edge_idx = bb_idx ^ prev_loc;
                uint32_t byte_offset = edge_idx/8;
                uint32_t bit = edge_idx%8;
                uint8_t new_byte = 1<<bit;
                m_data_c[byte_offset] |= new_byte;
                prev_loc = bb_idx >> 1;
                */
                gimple_seq hit_seq = NULL;

                if (blocks == 0) {
                    ploc = create_tmp_var(uint32_type_node, ".ploc");
                }
                gimple* load_ploc = gimple_build_assign(ploc, gploc);
                gimple_seq_add_stmt(&hit_seq, load_ploc);

                // edge_idx = bb_idx ^ prev_loc
                if (blocks == 0) {
                    edge_idx = create_tmp_var(uint32_type_node, ".edge_idx");
                }
                gimple* xor_loc = gimple_build_assign(
                    edge_idx, 
                    BIT_XOR_EXPR, 
                    ploc, bb_idx
                );
                gimple_seq_add_stmt(&hit_seq, xor_loc);

                // byte_offset = edge_idx >> 3
                if (blocks == 0) {
                    byte_offset = create_tmp_var(uint32_type_node, ".byte_offset");
                }
                gimple* calc_idx = gimple_build_assign(
                    byte_offset,
                    RSHIFT_EXPR,
                    edge_idx,
                    build_int_cst(uint32_type_node, 3)
                );
                gimple_seq_add_stmt(&hit_seq, calc_idx);
                
                // tgt_byte_ptr = &map_ptr[byte_offset]
                if (blocks == 0) {
                    dcov_mdata_ptr = create_tmp_var(uint8_ptr_type, ".dcov_map_ptr");
                    tgt_byte_ptr = create_tmp_var(uint8_ptr_type, ".target_byte_ptr");
                }
                gimple* idx_map = gimple_build_assign(
                    tgt_byte_ptr, POINTER_PLUS_EXPR, dcov_mdata_ptr, byte_offset
                );
                gimple_seq_add_stmt(&hit_seq, idx_map);

                // bit_offset = edge_idx % 8
                if (blocks == 0) {
                    bit_offset = create_tmp_var(uint8_type_node, ".bit_offset");
                }
                gimple* calc_bits = gimple_build_assign(
                    bit_offset,
                    TRUNC_MOD_EXPR,
                    edge_idx,
                    build_int_cst(uint8_type_node, 8)
                );
                gimple_seq_add_stmt(&hit_seq, calc_bits);

                // new_byte = 1 << bit_offset
                if (blocks == 0) {
                    new_byte = create_tmp_var(uint8_type_node, ".new_byte");
                }
                gimple* calc_new_byte = gimple_build_assign(
                    new_byte,
                    LSHIFT_EXPR,
                    build_int_cst(uint8_type_node, 1),
                    bit_offset
                );
                gimple_seq_add_stmt(&hit_seq, calc_new_byte);

                // *tgt_byte_ptr |= new_byte
                tree memmod = build_int_cst(integer_type_node, MEMMODEL_SEQ_CST);
                tree fxor = builtin_decl_explicit(BUILT_IN_ATOMIC_FETCH_OR_1);
                gimple* set_ntry = gimple_build_call(
                    fxor,
                    3,
                    tgt_byte_ptr,
                    new_byte,
                    memmod
                );
                gimple_seq_add_seq(&hit_seq, set_ntry);

                // ploc = bb_idx >> 1
                gimple* update_ploc = gimple_build_assign(
                    ploc,
                    build_int_cst(uint32_type_node, bb_idx_i>>1)
                );
                gimple_seq_add_stmt(&hit_seq, update_ploc);

                gimple_stmt_iterator insp = gsi_after_labels(bb);
                gsi_insert_seq_before(&insp, hit_seq, GSI_SAME_STMT);
                    
                blocks++;
            }
            // if (blocks) {
            //     printf("\033[32m[LEAVE] Instrumented %d edges\033[0m\n", blocks);
            // }else{
            //     printf("\033[32m[LEAVE] No edges Found\033[0m\n");
            // }

            bb_instrumented += blocks;

            if (blocks){
                gimple_seq seq = NULL;

                // getenv
                tree getenv_decl = get_getenv();
                tree atoi_decl = get_atoi();
                tree shmget_decl = get_shmget();
                tree shmat_decl = get_shmat();

                tree shm_key_str = create_tmp_var(char_ptr_type, ".dcov_shm_key_str");
                tree shm_key_int = create_tmp_var(integer_type_node, ".dcov_shm_key_int");
                tree shm_id = create_tmp_var(integer_type_node, ".dcov_shm_id");
                tree bytemap_size = build_int_cst(uint32_type_node, 1<<17);
                
                // // .dcov_shm_key_str = getenv("DCOV_KEY_C")
                tree env_str = build1(
                    CONVERT_EXPR, const_char_ptr_type, 
                    build_string_literal(strlen("DCOV_KEY_C")+1, "DCOV_KEY_C")
                );
                tree call_getenv = build1(
                    CONVERT_EXPR, char_ptr_type, 
                    build_call_expr(getenv_decl, 1, env_str)
                );
                gimple* get_shm_key_str = gimple_build_assign(
                    shm_key_str, 
                    call_getenv
                );
                gimple_seq_add_stmt(&seq, get_shm_key_str);
                
                
                // .dcov_shm_key_int = atoi(.dcov_shm_key_str);
                gimple* get_shm_key_int = gimple_build_assign(
                    shm_key_int, 
                    build1(
                        CONVERT_EXPR,
                        integer_type_node, 
                        build_call_expr(
                            atoi_decl, 
                            1, 
                            shm_key_str
                        )
                    )
                );
                gimple_seq_add_stmt(&seq, get_shm_key_int);
            
                // .dcov_shm_id = shmget(.dcov_shm_key_int, bytemap_size, IPC_CREAT | 0666);
                gimple* get_shmid = gimple_build_assign(
                    shm_id, 
                    build1(
                        CONVERT_EXPR,
                        integer_type_node, 
                        build_call_expr(
                            shmget_decl, 
                            3,
                            shm_key_int,
                            bytemap_size,
                            build_int_cst(integer_type_node, IPC_CREAT | 0666)
                        )
                    )
                );
                gimple_seq_add_stmt(&seq, get_shmid);

                // // dcov_mdata_ptr = (unsigned char*) shmat(shm_id, NULL, 0);
                gimple* get_mdata_ptr = gimple_build_assign(
                    dcov_mdata_ptr, 
                    build1(
                        CONVERT_EXPR,
                        uint8_ptr_type,
                        build_call_expr(
                            shmat_decl, 
                            3,
                            shm_id,
                            build_int_cst(void_ptr_type, 0),
                            build_int_cst(integer_type_node, 0)
                        )
                    )
                );
                gimple_seq_add_stmt(&seq, get_mdata_ptr);

                gimple* init_gploc = gimple_build_assign(
                    gploc, 
                    build_int_cst(uint32_type_node, 0)
                );
                gimple_seq_add_stmt(&seq, init_gploc);

                /* Insert it in the edge to the entry block.  We don't want to
                insert it in the first block, since there might be a loop
                or a goto back to it.  Insert in the edge, which may create
                another block.  */
                edge e = single_succ_edge(ENTRY_BLOCK_PTR_FOR_FN(fun));
                gsi_insert_seq_on_edge_immediate(e, seq);
            }

            return 0;
        }

        bool isIgnoreFunction(function *F) {

            // Starting from "LLVMFuzzer" these are functions used in libfuzzer based
            // fuzzing campaign installations, e.g. oss-fuzz

            static constexpr const char *ignoreList[] = {

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
                "identifyCallsites"
            };

            const char *name = IDENTIFIER_POINTER(DECL_NAME(F->decl));
            int         len = IDENTIFIER_LENGTH(DECL_NAME(F->decl));

            for (auto const &ignoreListFunc : ignoreList) {

                if (strncmp(name, ignoreListFunc, len) == 0) { return true; }

            }

            return false;
        }

        inline bool should_instrument_function(function* F){
            bool return_default = true;

            // is this a function with code? If it is external we don't instrument it
            // anyway and it can't be in the instrument file list. Or if it is it is
            // ignored.
            if (isIgnoreFunction(F)) return false;

            return return_default;

        }

        inline bool should_instrument_block(basic_block bb){
            edge          e;
            edge_iterator ei;
            FOR_EACH_EDGE(e, ei, bb->preds)
            if (!single_succ_p(e->src)) return true;

            return false;
        }

        static inline tree get_getenv(){
            tree char_ptr_type = build_pointer_type(char_type_node);
            tree const_char_ptr_type = build_qualified_type(char_ptr_type, TYPE_QUAL_CONST);
            tree getenv_type = build_function_type_list(char_ptr_type, const_char_ptr_type, NULL_TREE);
            tree getenv_decl = build_fn_decl("getenv", getenv_type);
            TREE_PUBLIC(getenv_decl) = 1; // 表示函数在外部定义
            DECL_EXTERNAL(getenv_decl) = 1; // 表示函数在外部定义
            DECL_ARTIFICIAL(getenv_decl) = 1;
            return getenv_decl;
        }

        static inline tree get_atoi(){
            tree char_ptr_type = build_pointer_type(char_type_node);
            tree const_char_ptr_type = build_qualified_type(char_ptr_type, TYPE_QUAL_CONST);
            tree atoi_type = build_function_type_list(integer_type_node, const_char_ptr_type, NULL_TREE);
            tree atoi_name = get_identifier("atoi");
            tree atoi_decl = build_decl(BUILTINS_LOCATION, FUNCTION_DECL, atoi_name, atoi_type);
            TREE_PUBLIC(atoi_decl) = 1; // 表示函数在外部定义
            DECL_EXTERNAL(atoi_decl) = 1; // 表示函数在外部定义
            return atoi_decl;
        }

        static inline tree get_shmget(){
            tree shmget_type = build_function_type_list(
                integer_type_node,
                integer_type_node,
                integer_type_node,
                integer_type_node,
                NULL_TREE
            );
            tree shmget_name = get_identifier("shmget");
            tree shmget_decl = build_decl(BUILTINS_LOCATION, FUNCTION_DECL, shmget_name, shmget_type);
            TREE_PUBLIC(shmget_decl) = 1; // 表示函数在外部定义
            DECL_EXTERNAL(shmget_decl) = 1; // 表示函数在外部定义
            return shmget_decl;
        }

        static inline tree get_shmat(){
            tree void_ptr_type = build_pointer_type(void_type_node);
            tree const_void_ptr_type = build_qualified_type(void_ptr_type, TYPE_QUAL_CONST);
            tree shmat_type = build_function_type_list(
                void_ptr_type,
                integer_type_node,
                const_void_ptr_type,
                integer_type_node,
                NULL_TREE
            );
            tree shmat_name = get_identifier("shmat");
            tree shmat_decl = build_decl(BUILTINS_LOCATION, FUNCTION_DECL, shmat_name, shmat_type);
            TREE_PUBLIC(shmat_decl) = 1; // 表示函数在外部定义
            DECL_EXTERNAL(shmat_decl) = 1; // 表示函数在外部定义
            return shmat_decl;
        }

        virtual dcov_pass* clone() override
        {
            // We do not clone ourselves
            return this;
        }
    };

    static void plugin_finalize(void *, void *p)
    {
        std::cerr << "\033[32mAll things done! Totally instruments \033[1;32m"<<bb_instrumented<<"\033[0;32m edges\033[0m\n";
    }

}

int plugin_init (struct plugin_name_args *plugin_info,
		struct plugin_gcc_version *version)
{
	if (!plugin_default_version_check (version, &gcc_version))
    {
        std::cerr << "This GCC plugin is for version " << GCCPLUGIN_VERSION_MAJOR << "." << GCCPLUGIN_VERSION_MINOR << "\n";
		return 1;
    }

    register_callback(plugin_info->base_name, PLUGIN_INFO, NULL, &dcov_plugin_info);


    struct register_pass_info pass_info{
        .pass = new dcov_pass(g),
        .reference_pass_name = "ssa",
        .ref_pass_instance_number = 1,
        .pos_op = PASS_POS_INSERT_AFTER
    };

    register_callback (plugin_info->base_name, PLUGIN_PASS_MANAGER_SETUP, NULL, &pass_info);
    register_callback (plugin_info->base_name, PLUGIN_FINISH, plugin_finalize, NULL);

    return 0;
}