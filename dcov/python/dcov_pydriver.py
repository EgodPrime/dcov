import argparse
import sys

from dcov.python.dcov_loader import DcovMetaPathFinder


def main():
    argparser = argparse.ArgumentParser(description="Driver for Dcov")
    argparser.add_argument("-t", "--coverage_type", help="one of [branch, function, block, edge]")
    argparser.add_argument("-s", "--source", nargs="*", help="target library source directory")
    argparser.add_argument(
        "rargs", nargs=argparse.REMAINDER, help='Remaining arguments to pass to the target program"'
    )
    args = argparse.parse_args()
    cov_type = args.coverage_type
    sources = args.source

    mpf = DcovMetaPathFinder(cov_type)
    mpf.sources.extend(sources)
    sys.meta_path.insert(0, mpf)


if __name__ == "__main__":
    main()
