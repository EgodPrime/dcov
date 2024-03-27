from utils.skip import need_skip_torch
import configparser
from os.path import join, abspath
import subprocess
from utils.printer import dump_data
import argparse
import time
import sys
sys.path.append(abspath('../../../../..'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FreeFuzz: a fuzzing frameword for deep learning library")
    parser.add_argument("--conf", type=str, default="demo.conf", help="configuration file")
    args = parser.parse_args()

    config_name = args.conf
    freefuzz_cfg = configparser.ConfigParser()
    freefuzz_cfg.read(join(__file__.replace("FreeFuzz.py", "config"), config_name))

    libs = freefuzz_cfg["general"]["libs"].split(",")
    print("Testing on ", libs)
    
    mongo_cfg = freefuzz_cfg["mongodb"]
    host = mongo_cfg["host"]
    port = int(mongo_cfg["port"])

    # output configuration
    output_cfg = freefuzz_cfg["output"]
    torch_output_dir = output_cfg["torch_output"]
    tf_output_dir = output_cfg["tf_output"]

    from dcov import dcov
    dcov.init_bitmap()
    
    use_feedback = freefuzz_cfg['dcov']['use_feedback']
    api_num_limit = int(freefuzz_cfg['dcov']['api_num_limit'])
    
    if "torch" in libs:
        f = open(join(abspath('../..'), f'freefuzz_pt_{use_feedback}.txt'), 'w')
        f.write('iteration,time_used(s),python_coverage,c_coverage\n')
        # database configuration
        from classes.database import TorchDatabase
        TorchDatabase.database_config(host, port, mongo_cfg["torch_database"])
        iteration = 0
        time_start = time.time()
        for api_name in TorchDatabase.get_api_list():
            print(api_name)
            if need_skip_torch(api_name):
                continue
            try:
                res = subprocess.run(["python3", "FreeFuzz_api.py", config_name, "torch", api_name], shell=False, timeout=100)
            except subprocess.TimeoutExpired:
                dump_data(f"{api_name}\n", join(torch_output_dir, "timeout.txt"), "a+")
            except Exception as e:
                dump_data(f"{api_name}\n  {e}\n", join(torch_output_dir, "runerror.txt"), "a+")
            else:
                if res.returncode != 0:
                    dump_data(f"{api_name}\n", join(torch_output_dir, "runcrash.txt"), "a+")
            cov_py,cov_c = dcov.get_bb_cnts()
            time_now = time.time() - time_start
            f.write(f"{iteration},{time_now},{cov_py},{cov_c}\n")
            f.flush()
            iteration += 1
            if iteration >= api_num_limit:
                break
        f.close()
        
    if "tf" in libs:
        f = open(join(abspath('../..'), f'freefuzz_tf_{use_feedback}.txt'), 'w')
        f.write('iteration,time_used(s),python_coverage,c_coverage\n')
        # database configuration
        from classes.database import TFDatabase
        TFDatabase.database_config(host, port, mongo_cfg["tf_database"])
        iteration = 0
        time_start = time.time()
        for api_name in TFDatabase.get_api_list():
            print(api_name)
            try:
                res = subprocess.run(["python3", "FreeFuzz_api.py", config_name, "tf", api_name], shell=False, timeout=100)
            except subprocess.TimeoutExpired:
                dump_data(f"{api_name}\n", join(tf_output_dir, "timeout.txt"), "a")
            except Exception as e:
                dump_data(f"{api_name}\n  {e}\n", join(tf_output_dir, "runerror.txt"), "a")
            else:
                if res.returncode != 0:
                    dump_data(f"{api_name}\n", join(tf_output_dir, "runcrash.txt"), "a")
            cov_py,cov_c = dcov.get_bb_cnts()
            time_now = time.time() - time_start
            f.write(f"{iteration},{time_now},{cov_py},{cov_c}\n")
            f.flush()
            iteration += 1
            if iteration >= api_num_limit:
                break
        f.close()
    
    not_test = []
    for l in libs:
        if l not in ["tf", "torch"]: not_test.append(l)
    if len(not_test):
        print(f"WE DO NOT SUPPORT SUCH DL LIBRARY: {not_test}!")
