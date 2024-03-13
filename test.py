from . import dcov



if __name__ == "__main__":
    import os
    import subprocess

    root_dir = '/root/benchmark'
    python_bins = {
        'tf':'/root/miniconda3/envs/tf2.11.0-ins/bin/python',
        'torch':'/root/miniconda3/envs/torch2.1.0-ins/bin/python',
        'paddle':'/root/miniconda3/envs/paddle2.5-ins/bin/python',
        'oneflow':'/root/miniconda3/envs/oneflow0.9.0-ins/bin/python',
    }

    dcov.init_bitmap_python()

    for dir_path, dirnames, _ in os.walk(root_dir):
        for dirname in dirnames:
            print(f'walking {dirname}')
            for dirpath, _, filenames in os.walk(os.path.join(dir_path, dirname)):
                for filename in filenames:
                    # 检查文件是否以 .py 结尾
                    if filename.endswith('.py'):
                        # 构建文件的完整路径
                        file_path = os.path.join(dirpath, filename)
                        print(f'Executing: {file_path}')
                        # 执行找到的 Python 脚本
                        try:
                            subprocess.run([python_bins[dirname], file_path], check=True)
                            print(dcov.get_bb_cnt_python())
                        except subprocess.CalledProcessError as e:
                            print(f"Error executing {file_path}: {e}")