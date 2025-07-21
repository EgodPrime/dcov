import pathlib

import dcov


def main():
    dcov.open_bitmap_c()
    dcov.open_bitmap_py()
    # you can change the 'cov_type' from ['branch','edge','function']
    # If you don't set the 'cov_type', change LoaderWrapper(cov_type) to LoaderWrapper(), and it will be 'edge' mode
    # cov_type = 'branch'
    cov_type = "line"
    # cov_type = 'block'
    # cov_type = 'edge'
    print(f"Testing {cov_type} coverage")
    with dcov.LoaderWrapper(cov_type) as loader:
        loader.add_source(pathlib.Path.cwd())
        from example import test_py

        print(f"Coverage before test_switch(1, 1): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(1, 1)
        print(f"Coverage before test_switch(1, 2): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(1, 2)
        print(f"Coverage before test_switch(1, 3): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(1, 3)
        print(f"Coverage before test_switch(1, 4): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(1, 4)
        print(f"Coverage before test_switch(0, 1): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(0, 1)
        print(f"Coverage before test_switch(0, 2): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(0, 2)
        print(f"Coverage before test_switch(0, 3): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(0, 3)
        print(f"Coverage before test_switch(0, 4): {dcov.count_bits_py()},{dcov.count_bits_c()}")
        test_py(0, 4)
        print(f"Final Coverage: {dcov.count_bits_c()}")
        dcov.clear_bitmap_c()
        dcov.clear_bitmap_py()
    dcov.close_bitmap_py()
    dcov.close_bitmap_c()


if __name__ == "__main__":
    main()
