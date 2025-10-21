import importlib
import importlib.util
import sys

import fire

import dcov


def __main(lib_name: str, tc_path: str):
    spec = importlib.util.find_spec(lib_name)
    if spec is None:
        print(f"Library {lib_name} not found.", file=sys.__stderr__)
        return
    origin = spec.origin
    if origin is None:
        print(f"Library {lib_name} does not have an origin.", file=sys.__stderr__)
        return

    dcov.clear_bitmap_x(4399)
    print("Start instrument")

    code = open(tc_path, "r").read()
    with dcov.LoaderWrapper() as lw:
        lw.add_source(origin)
        exec(code)

    # print(f"Python line coverage of {tc_path} is {dcov.count_bits_x(4399)}")


def main():
    fire.Fire(__main)


if __name__ == "__main__":
    main()
