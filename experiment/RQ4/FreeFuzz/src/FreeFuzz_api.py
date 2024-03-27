import sys
from constants.enum import OracleType
import configparser
from os.path import join, abspath
from utils.converter import str_to_bool
import math
sys.path.append(abspath('../../../../..'))


class MutationBandit:
    def __init__(self, records, api_name):

        self.arms = [f"{api_name}_{i}" for i in range(len(records))]
        self.records = {f"{api_name}_{i}": record for i, record in enumerate(records)}
        self.counts = {arm: 0 for arm in self.arms}  
        self.values = {arm: 0.0 for arm in self.arms}  

    def select_arm(self):
        total_counts = sum(self.counts.values())
        log_total = math.log(total_counts + 1)
        ucb_values = {
            arm: (self.values[arm] + math.sqrt((2 * log_total) / (self.counts[arm] + 1)))
            for arm in self.arms
        }
        return max(ucb_values, key=ucb_values.get)

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]
        value = self.values[chosen_arm]
        self.values[chosen_arm] = ((n - 1) / float(n)) * value + (1 / float(n)) * reward


if __name__ == "__main__":
    config_name = sys.argv[1]
    library = sys.argv[2]
    api_name = sys.argv[3]

    freefuzz_cfg = configparser.ConfigParser()
    freefuzz_cfg.read(join(__file__.replace("FreeFuzz_api.py", "config"), config_name))

    # database configuration
    mongo_cfg = freefuzz_cfg["mongodb"]
    host = mongo_cfg["host"]
    port = int(mongo_cfg["port"])

    # oracle configuration
    oracle_cfg = freefuzz_cfg["oracle"]
    crash_oracle = str_to_bool(oracle_cfg["enable_crash"])
    cuda_oracle = str_to_bool(oracle_cfg["enable_cuda"])
    precision_oracle = str_to_bool(oracle_cfg["enable_precision"])

    diff_bound = float(oracle_cfg["float_difference_bound"])
    time_bound = float(oracle_cfg["max_time_bound"])
    time_thresold = float(oracle_cfg["time_thresold"])

    # output configuration
    output_cfg = freefuzz_cfg["output"]
    torch_output_dir = output_cfg["torch_output"]
    tf_output_dir = output_cfg["tf_output"]
    
    from dcov import dcov
    # dcov.open_bitmap_python()
    dcov.open_bitmap()
    dcov.insert_slipcover()
    use_feedback = True if freefuzz_cfg['dcov']['use_feedback']=='true' else False
    print(f"use_feedback={use_feedback}")
    
    # mutation configuration
    mutation_cfg = freefuzz_cfg["mutation"]
    enable_value = str_to_bool(mutation_cfg["enable_value_mutation"])
    enable_type = str_to_bool(mutation_cfg["enable_type_mutation"])
    enable_db = str_to_bool(mutation_cfg["enable_db_mutation"])
    each_api_run_times = int(mutation_cfg["each_api_run_times"])

    if library.lower() in ["pytorch", "torch"]:
        import torch
        from classes.torch_library import TorchLibrary
        from classes.torch_api import TorchAPI
        from classes.database import TorchDatabase
        from utils.skip import need_skip_torch

        TorchDatabase.database_config(host, port, mongo_cfg["torch_database"])

        if cuda_oracle and not torch.cuda.is_available():
            print("YOUR LOCAL DOES NOT SUPPORT CUDA")
            cuda_oracle = False
        # Pytorch TEST
        if use_feedback:
            records = TorchDatabase.get_all_records(api_name)
            bandit = MutationBandit(records, api_name)
            
        MyTorch = TorchLibrary(torch_output_dir, diff_bound, time_bound,
                            time_thresold)
        for _ in range(each_api_run_times):
            if use_feedback:
                chosen_arm = bandit.select_arm()
                print(chosen_arm)
                api = TorchAPI(api_name, bandit.records[chosen_arm])
                api.mutate(enable_value, enable_type, False)
            else:
                api = TorchAPI(api_name)
                api.mutate(enable_value, enable_type, enable_db)
            
            if use_feedback:
                cov_py,cov_c = dcov.get_bb_cnts()
           
            if crash_oracle:
                MyTorch.test_with_oracle(api, OracleType.CRASH)
            if cuda_oracle:
                MyTorch.test_with_oracle(api, OracleType.CUDA)
            if precision_oracle:
                MyTorch.test_with_oracle(api, OracleType.PRECISION)
            
            if use_feedback:
                py_cov_gain = dcov.get_bb_cnt_python() - cov_py
                c_cov_gain = dcov.get_bb_cnt_c() - cov_c
                norm_py_gain = int(py_cov_gain>0)
                norm_c_gain = int(c_cov_gain>0)
                reward = norm_py_gain + norm_c_gain
                bandit.update(chosen_arm, reward)
                
    elif library.lower() in ["tensorflow", "tf"]:
        import tensorflow as tf
        from classes.tf_library import TFLibrary
        from classes.tf_api import TFAPI
        from classes.database import TFDatabase
        from utils.skip import need_skip_tf

        TFDatabase.database_config(host, port, mongo_cfg["tf_database"])
        if cuda_oracle and not tf.test.is_gpu_available():
            print("YOUR LOCAL DOES NOT SUPPORT CUDA")
            cuda_oracle = False
        if use_feedback:
            records = TFDatabase.get_all_records(api_name)
            bandit = MutationBandit(records, api_name)
        MyTF = TFLibrary(tf_output_dir, diff_bound, time_bound,
                            time_thresold)
        print(api_name)
        if need_skip_tf(api_name): pass
        else:
            for _ in range(each_api_run_times):
                api = TFAPI(api_name)
                if use_feedback:
                    chosen_arm = bandit.select_arm()
                    print(f"chosen_arm={chosen_arm}")
                    api = TFAPI(api_name, bandit.records[chosen_arm])
                    api.mutate(enable_value, enable_type, False)
                else:
                    api = TFAPI(api_name)
                    api.mutate(enable_value, enable_type, enable_db)
                    
                if use_feedback:
                    cov_py,cov_c = dcov.get_bb_cnts()
                    
                if crash_oracle:
                    MyTF.test_with_oracle(api, OracleType.CRASH)
                if cuda_oracle:
                    MyTF.test_with_oracle(api, OracleType.CUDA)
                if precision_oracle:
                    MyTF.test_with_oracle(api, OracleType.PRECISION)
                    
                if use_feedback:
                    py_cov_gain = dcov.get_bb_cnt_python() - cov_py
                    c_cov_gain = dcov.get_bb_cnt_c() - cov_c
                    norm_py_gain = int(py_cov_gain>0)
                    norm_c_gain = int(c_cov_gain>0)
                    reward = norm_py_gain + norm_c_gain
                    bandit.update(chosen_arm, reward)

    else:
        print(f"WE DO NOT SUPPORT SUCH DL LIBRARY: {library}!")
