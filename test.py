import dcov



if __name__ == "__main__":
    import os
    import time

    root_dir = '/root/benchmark'

    dcov.init_bitmap()
    # dcov.init_bitmap_python()
    # dcov.init_bitmap_c()

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
                        with open(file_path, 'r') as f:
                            code = f.read()
                            exec(code)
                        s = time.time_ns()
                        print(dcov.get_bb_cnts())
                        e = time.time_ns()
                        print(f"It takes {e-s} ns to get Python coverage and C coverage")
                        # print(dcov.get_bb_cnt_python())
                        # print(dcov.get_bb_cnt_c())
