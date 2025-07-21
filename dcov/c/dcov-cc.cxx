#include <cstdlib>
#include <string.h>
#include <string>
#include <vector>
#include <unistd.h>
#include <iostream>
#include <cstring>

int main(int argc, char **argv) {
    // 1. 获取原始 GCC 路径（默认是系统 GCC）
    std::string cc_name = argv[0];
    std::string real_cc_path;
    if (cc_name.rfind("dcov-gcc")!=std::string::npos){
        real_cc_path = "gcc";
    }else if (cc_name.rfind("dcov-g++")!=std::string::npos){
        real_cc_path = "g++";
    }else if (cc_name.rfind("dcov-clang++")!=std::string::npos){
        real_cc_path = "clang++";
    }else if (cc_name.rfind("dcov-clang")!=std::string::npos){
        real_cc_path = "clang";
    }else{
        std::cout<<"Error: Unknown compiler name."<<std::endl;
        return 1;
    }
    
    // 2. 构造新的参数列表
    std::vector<std::string> new_args;
    new_args.push_back(real_cc_path);  // 第一个参数是编译器路径

    // 3. 传递用户的其他参数
    bool has__o= false;
    bool has__c=false;
    for (int i = 1; i < argc; i++) {
        // 删掉-O
        // if (!strcmp(argv[i], "-O1") || !strcmp(argv[i], "-O2") || !strcmp(argv[i], "-O3") || !strcmp(argv[i], "-O4")) {
        //     continue;
        // }
        // 是否有-o

        // 禁用-Werror
        if (strstr(argv[i], "-Werror,")){
            continue;
        }
        if (!strcmp(argv[i], "-o")) {
            has__o = true;
        }
        // 是否有-c
        if (!strcmp(argv[i], "-c")) {
            has__c = true;
        }
        
        new_args.push_back(argv[i]);
    }

    // 4. 生成对象时添加插桩参数
    if (has__c || has__o){
        new_args.push_back("-g");
        new_args.push_back("-O0");
        if (cc_name.find("dcov-gcc") != std::string::npos || cc_name.find("dcov-g++") != std::string::npos){ 
            new_args.push_back("-fplugin=libdcov_gimple.so");
            // new_args.push_back("-fcf-protection=full");
            // new_args.push_back("-fno-if-conversion");
            // new_args.push_back("-fno-if-conversion2");
            // new_args.push_back("-static-libasan");
        }
        else if (cc_name.find("dcov-clang") != std::string::npos || cc_name.find("dcov-clang++") != std::string::npos){
            new_args.push_back("-fpass-plugin=libdcov_llvm_pass.so");
            new_args.push_back("-fexperimental-new-pass-manager");
        }
    }

    // 5. 将new_args转化为c_string 数组
    std::vector<char *> new_args_cstr(new_args.size() + 1);  // +1 用于存储 NULL
    for (size_t i = 0; i < new_args.size(); i++) {
        new_args_cstr[i] = const_cast<char *>(new_args[i].c_str());
    }
    new_args_cstr[new_args.size()] = nullptr;

    new_args_cstr.push_back(nullptr);  // execvp 要求以 NULL 结尾

    // // 打印新的完整的编译命令
    // printf("\n\033[32m%s ",real_cc_path.c_str());
    // for (size_t i = 1; new_args_cstr[i] != nullptr; i++) {
    //     printf("%s ", new_args_cstr[i]);
    // }
    // printf("\n\033[0m\n");

    // 6. 调用真实 GCC
    execvp(real_cc_path.c_str(), new_args_cstr.data());

    // 如果执行到这里，说明 execvp 失败了
    std::cerr << "dcov-cc: Failed to execute " << real_cc_path << "\n";
    return EXIT_FAILURE;
}