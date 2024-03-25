import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot(libname):
    base_file_path = f'./{libname}_base.txt'
    dcov_file_path = f'./{libname}_dcov.txt'

    # Loading the data into DataFrames
    base_df = pd.read_csv(base_file_path)
    dcov_df = pd.read_csv(dcov_file_path)

    # plt.figure(figsize=(21, 6))

    # # Plot 1: Iteration vs Time Used
    # plt.subplot(1, 3, 1)
    # plt.plot(base_df['iteration'], base_df['time_used(ms)'], color='blue', label='Base')
    # plt.plot(dcov_df['iteration'], dcov_df['time_used(ms)'], color='green', label='Dcov')
    # plt.xlabel('Iteration')
    # plt.ylabel('Time Used (ms)')
    # plt.title('Iteration vs Time Used')
    # plt.legend()

    # # Plot 2: Iteration vs Python Coverage
    # plt.subplot(1, 3, 2)
    # plt.plot(dcov_df['iteration'], dcov_df['python_coverage'], color='orange', label='Python Coverage')
    # plt.xlabel('Iteration')
    # plt.ylabel('Python Coverage')
    # plt.title('Iteration vs Python Coverage')
    # plt.legend()

    # # Plot 3: Iteration vs C Coverage
    # plt.subplot(1, 3, 3)
    # plt.plot(dcov_df['iteration'], dcov_df['c_coverage'], color='red', label='C Coverage')
    # plt.xlabel('Iteration')
    # plt.ylabel('C Coverage')
    # plt.title('Iteration vs C Coverage')
    # plt.legend()
    
    plt.figure(figsize=(16, 9))

    # Adjusted first plot (iteration vs time_used) with different colors
    plt.subplot(1, 2, 1)
    plt.plot(base_df['iteration'], base_df['time_used(ms)'], color='blue', label='Base')
    plt.plot(dcov_df['iteration'], dcov_df['time_used(ms)'], color='green', label='Dcov')
    plt.xlabel('Iteration')
    plt.ylabel('Time Used (ms)')
    plt.title('Iteration vs Time Used')
    plt.legend()

    # Adjusted second plot (iteration vs coverage) with separate lines for python_coverage and c_coverage
    plt.subplot(1, 2, 2)
    plt.plot(dcov_df['iteration'], dcov_df['python_coverage'], color='orange', label='Python Coverage')
    plt.plot(dcov_df['iteration'], dcov_df['c_coverage'], color='red', label='C Coverage')
    plt.xlabel('Iteration')
    plt.ylabel('Coverage')
    plt.title('Iteration vs Coverage')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'RQ1_{libname}.png', dpi=300)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--libname', type=str, required=True, choices=['tensorflow','torch','paddle'])
    args = parser.parse_args()
    libname = args.libname
    plot(libname)
    