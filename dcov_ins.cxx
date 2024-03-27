#include "gcc-plugin.h"
#include "plugin-version.h"

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

#include "dcov.h"
#include "MurmurHash3.h"

#include <iostream>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>

int plugin_is_GPL_compatible;

static int shmid;
static unsigned char* m_data;

static bool __init__shm__ = [](){
    shmid = shmget(4401, 4, IPC_CREAT | 0666);
    m_data = (unsigned char*) shmat(shmid, NULL, 0);
    return true;
}();

static struct plugin_info dcov_plugin_info = {
  .version = "1.0",
  .help = "Track every bb execution",
};

uint32_t get_bb_id(){
    unsigned int id;
    unsigned int new_id;
    do
    {
        id = __atomic_load_4(m_data, __ATOMIC_SEQ_CST);
        new_id = id + 1;
    }
    while (!__atomic_compare_exchange_4(m_data, &id, new_id, false, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST));
    return new_id;
}

namespace
{
  int bb_instrumented = 0;

  const pass_data dcov_ins_pass_data = 
  {
      GIMPLE_PASS,
      "dcov",        /* name */
      OPTGROUP_NONE,          /* optinfo_flags */
      TV_NONE,                /* tv_id */
      PROP_gimple_any,        /* properties_required */
      0,                      /* properties_provided */
      0,                      /* properties_destroyed */
      0,                      /* todo_flags_start */
      0                       /* todo_flags_finish */
  };

  uint32_t hash_bb(function*fun, basic_block bb){
    uint32_t hash;
    char str[256] {'\0'};
    strcat(str, function_name(fun));
    char bb_idx_str[16] = {0};
    sprintf(bb_idx_str, "%d",bb->index);
    strcat(str, bb_idx_str);
    MurmurHash3_x86_32(str, strlen(str), 0, &hash);
    return hash % bitmap_size;
  }

  struct dcov_ins_pass : gimple_opt_pass
  {
    dcov_ins_pass(gcc::context *ctx)
        : gimple_opt_pass(dcov_ins_pass_data, ctx)
    {   
    }

    virtual unsigned int execute(function *fun) override
    {      
        if(!fun) return 0;
        const char* fun_name = function_name(fun);
        const char* file_name = LOCATION_FILE(fun->function_start_locus);

        // skip unkown files
        if(!file_name) return 0;
        // skip headers
        if(strstr(file_name, ".h")!=NULL) return 0;

        // skip lambda
        if(!strcmp(IDENTIFIER_POINTER(DECL_NAME(fun->decl)),"<lambda>")) return 0;
        if(strstr(fun_name, "anonymous")!=NULL) return 0;
        if(strstr(fun_name, "operator")!=NULL) return 0;
        // skil main
        if(!strcmp(fun_name,"main"))  return 0;

        tree bb_type = build_function_type_list(void_type_node, uint32_type_node, NULL_TREE);
        tree bb_decl = build_fn_decl("on_bb_hit_c", bb_type);

        std::cerr << "\033[36m[ENTRY] "
                << function_name(fun) << " at "
                << (LOCATION_FILE(fun->function_start_locus) ? : "<unknown>") << ":" << LOCATION_LINE(fun->function_start_locus)<<"\n";
        std::cerr<<"\033[0m";

        basic_block bb;
        gimple_stmt_iterator gsi;
        gimple* stmt;
        tree arg;
        FOR_ALL_BB_FN(bb, fun)
        {   
            #ifdef DCOV_DEBUG
            std::cerr<<"\tHandle basic block "<<bb->index<<"...\n";
            #endif
            if(bb->index<2) {
                #ifdef DCOV_DEBUG
                std::cerr<<"\tSkip!\n";
                #endif
                continue;
            }

            gsi = gsi_start_bb(bb);
            gimple* first_stmt = gsi_stmt(gsi);
            if(first_stmt==NULL){
                #ifdef DCOV_DEBUG
                std::cerr<<"\tThe first statement is NULL...why?\n";
                #endif
                continue;
            } 
            auto stmt_type = gimple_code(first_stmt);

            #ifdef DCOV_DEBUG
            std::cerr<<"\tBefore any operations:\n";
            std::cerr<<"\tFirst statement type is "<<gimple_code_name[stmt_type]<<"\n";
            debug_bb(bb);
            verify_flow_info();
            #endif

            // skip exception handling edge
            #ifdef DCOV_DEBUG
            std::cerr<<"\Check if next to exception handling edge...\n";
            #endif
            bool is_exception_edge = false;
            edge e;
            edge_iterator ei;
            FOR_EACH_EDGE(e, ei, bb->preds)
            {
                if (e->flags & EDGE_ABNORMAL)
                {
                    is_exception_edge = true;
                    break;
                }
            }
            if (is_exception_edge){
                #ifdef DCOV_DEBUG
                std::cerr<<"\tSkip exception handling edge.\n";
                #endif
                continue;
            } 

            // arg = build_int_cst(uint32_type_node, hash_bb(fun, bb));
            arg = build_int_cst(uint32_type_node, get_bb_id());
            stmt = gimple_build_call(bb_decl, 1, arg);
            switch(stmt_type){
                // case GIMPLE_LABEL:
                //     gsi_insert_after(&gsi, stmt, GSI_SAME_STMT);
                //     break;
                case GIMPLE_COND: case GIMPLE_GOTO: case GIMPLE_LABEL:
                    break;
                default:
                    gsi_insert_before(&gsi, stmt, GSI_SAME_STMT);
                    break;
            }
           
            #ifdef DCOV_DEBUG
            std::cerr<<"\tAfter insert:\n";
            debug_bb(bb);
            verify_flow_info();
            #endif

            bb_instrumented++;
            #ifdef DCOV_DEBUG
            std::cerr<<"\tInstruments with "<<hash_bb(fun, bb)<<"\n";
            #endif
        }
        std::cerr << "\033[36m[EXIT] "
            << function_name(fun) << " at "
            << (LOCATION_FILE(fun->function_end_locus) ? : "<unknown>") << ":" << LOCATION_LINE(fun->function_end_locus)<<"\n";
        std::cerr<<"\033[0m";
        // Nothing special todo
        return 0;
    }

    virtual dcov_ins_pass* clone() override
    {
        // We do not clone ourselves
        return this;
    }
  };
}

namespace {
    void finish_gcc(void *gcc_data, void *user_data)
    {
        std::cerr << "\033[32mAll things done! Totally instruments \033[1;32m"<<bb_instrumented<<"\033[0;32m basic blocks\033[0m\n";

        // int fd = open("/tmp/dcov_cnt", O_CREAT|O_RDWR);
        // if (fd == -1) {
        //     std::cerr << "Failed to open file" << std::endl;
        // }

        // /* Use the file lock to ensure the consistance in the concurrency cnodition*/
        // struct flock fl;
        // fl.l_type = F_WRLCK;
        // fl.l_whence = SEEK_SET;
        // fl.l_start = 0;
        // fl.l_len = 0;
        // fl.l_pid = getpid();
        // if (fcntl(fd, F_SETLKW, &fl) == -1) {
        //     std::cerr << "Failed to acquire lock" << std::endl;
        // }

        // uint32_t bb_cnt;
        // char buf[4];
        // read(fd, buf, sizeof(bb_cnt));
        // memcpy(&bb_cnt,buf,sizeof(bb_cnt));

        // std::cerr << "Read previous bb cnt: " << bb_cnt << std::endl;

        // bb_cnt += bb_instrumented;

        // std::cerr << "Write new bb cnt: " << bb_cnt << std::endl;

        // fseek(fdopen(fd,"w+"),0, SEEK_SET);
        // memcpy(buf,&bb_cnt,sizeof(bb_cnt));
        // write(fd, buf, sizeof(bb_cnt));

        // fl.l_type = F_UNLCK;
        // if (fcntl(fd, F_SETLKW, &fl) == -1) {
        //     std::cerr << "Failed to release lock" << std::endl;
        // }

        // close(fd);

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

    register_callback(plugin_info->base_name,
            /* event */ PLUGIN_INFO,
            /* callback */ NULL, /* user_data */ &dcov_plugin_info);

    // Register the phase right after omplower
    struct register_pass_info pass_info;

    pass_info.pass = new dcov_ins_pass(g);
    pass_info.reference_pass_name = "ssa";
    pass_info.ref_pass_instance_number = 1;
    pass_info.pos_op = PASS_POS_INSERT_BEFORE;

    register_callback (plugin_info->base_name, PLUGIN_PASS_MANAGER_SETUP, NULL, &pass_info);
    register_callback (plugin_info->base_name, PLUGIN_FINISH, finish_gcc, NULL);

    return 0;
}