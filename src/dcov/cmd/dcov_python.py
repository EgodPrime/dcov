import fire

import dcov


def __main(lib_name: str, tc_path: str, cov_type: str = "line"):
    """
    Run the given test case file with coverage instrumentation for the specified library and coverage type.

    Args:
        lib_name (str): The name of the library to instrument.
        tc_path (str): The path to the test case file to execute.
        cov_type (str, optional): The type of coverage to collect ("line", "branch", "function", "block", "edge".). Defaults to "line".
    """
    bm = dcov.BitmapManager(4399)
    code = open(tc_path, "r").read()
    with dcov.LoaderWrapper(bm, cov_type, lib_name) as lw:
        exec(code)

    print(f"Python line coverage of {tc_path} is {bm.count_bitmap()}")


def main():
    fire.Fire(__main)


if __name__ == "__main__":
    main()
