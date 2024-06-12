import pandas as pd
import matplotlib.pyplot as plt

def load_data(libname:str):
    base_file_path = f'./{libname}_base.txt'
    dcov_file_path = f'./{libname}_dcov.txt'
    base_df = pd.read_csv(base_file_path)
    dcov_df = pd.read_csv(dcov_file_path)
    return base_df, dcov_df

def subplot(idx, libname, base_df, dcov_df):
    # Adjusted first plot (iteration vs time_used) with different colors
    plt.subplot(2, 3, idx)
    plt.plot(base_df['iteration'], base_df['time_used(ms)'], color='blue', label='Base')
    plt.plot(dcov_df['iteration'], dcov_df['time_used(ms)'], color='green', label='Dcov')
    plt.xlabel('Iteration of Scripts')
    plt.ylabel('Time Used (ms)')
    plt.title(f'Iteration vs. Time Used ({libname})')
    plt.legend()

    # Adjusted second plot (iteration vs coverage) with separate lines for python_coverage and c_coverage
    plt.subplot(2, 3, idx+3)
    plt.plot(dcov_df['iteration'], dcov_df['python_coverage'], color='orange', label='Python Coverage')
    plt.plot(dcov_df['iteration'], dcov_df['c_coverage'], color='red', label='C Coverage')
    plt.xlabel('Iteration of Scripts')
    plt.ylabel('Coverage')
    plt.title(f'Iteration vs. Coverage ({libname})')
    plt.legend()
    
def plot():
    tf_base_df, tf_dcov_df = load_data('tensorflow')
    pt_base_df, pt_dcov_df = load_data('torch')
    pp_base_df, pp_dcov_df = load_data('paddle')

    plt.figure(figsize=(16, 5))

    subplot(1, 'TensorFlow', tf_base_df, tf_dcov_df)
    subplot(2, 'PyTorch', pt_base_df, pt_dcov_df)
    subplot(3, 'PaddlePaddle', pp_base_df, pp_dcov_df)

    plt.tight_layout()
    plt.savefig(f'RQ1.png', dpi=300)

if __name__ == '__main__':
    plot()
    