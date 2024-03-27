# First, let's load and inspect the content of both files to understand their structure and data.
import pandas as pd
import matplotlib.pyplot as plt

# Load the content of the files
file_path_tf_false = 'freefuzz_tf_false.txt'
file_path_tf_true = 'freefuzz_tf_true.txt'
file_path_pt_false = 'freefuzz_pt_false.txt'
file_path_pt_true = 'freefuzz_pt_true.txt'

# Reading the content of the files
df_tf_false = pd.read_csv(file_path_tf_false)
df_tf_true = pd.read_csv(file_path_tf_true)
df_pt_false = pd.read_csv(file_path_pt_false)
df_pt_true = pd.read_csv(file_path_pt_true)

# Merging data on 'iteration' to simplify plotting
df_tf_merged = pd.merge(df_tf_false[['iteration', 'time_used(s)', 'python_coverage', 'c_coverage']],
                     df_tf_true[['iteration', 'time_used(s)', 'python_coverage', 'c_coverage']],
                     on='iteration', suffixes=('_false', '_true'))
df_pt_merged = pd.merge(df_pt_false[['iteration', 'time_used(s)', 'python_coverage', 'c_coverage']],
                     df_pt_true[['iteration', 'time_used(s)', 'python_coverage', 'c_coverage']],
                     on='iteration', suffixes=('_false', '_true'))

# Setting up the figure and axes for plotting
fig = plt.figure(figsize=(16, 5))

# Titles for each subplot
titles = ['Time Used (s)', 'Python Coverage', 'C Coverage']

# Iterating over each feature to plot
for i, feature in enumerate(['time_used(s)', 'python_coverage', 'c_coverage']):
    left = 0.33333333*(i+1)-0.12
    ax = plt.subplot(2, 3, i+1)
    # Plotting for both conditions
    ax.plot(df_tf_merged['iteration'], df_tf_merged[f'{feature}_false'], label='No Feedback', color='blue')
    ax.plot(df_tf_merged['iteration'], df_tf_merged[f'{feature}_true'], label='Feedback', color='orange')
    ax.set_title(f"TensorFlow-{titles[i]}")
    ax.set_xlabel('Iteration')
    ax.set_ylabel(titles[i])
    ax.legend(loc='upper left')
    inset_ax = fig.add_axes([left, 0.65, 0.1, 0.1])
    inset_ax.plot(df_tf_merged['iteration'][-50:], df_tf_merged[f'{feature}_false'][-50:], color='blue')
    inset_ax.plot(df_tf_merged['iteration'][-50:], df_tf_merged[f'{feature}_true'][-50:], color='orange')
    inset_ax.set_xticks([])
    
    ax = plt.subplot(2, 3, i + 4)
    ax.plot(df_pt_merged['iteration'], df_pt_merged[f'{feature}_false'], label='No Feedback', color='blue')
    ax.plot(df_pt_merged['iteration'], df_pt_merged[f'{feature}_true'], label='Feedback', color='orange')
    ax.set_title(f"PyTorch-{titles[i]}")
    ax.set_xlabel('Iteration')
    ax.set_ylabel(titles[i])
    ax.legend(loc='upper left')
    inset_ax = fig.add_axes([left, 0.16, 0.1, 0.1])
    inset_ax.plot(df_pt_merged['iteration'][-50:], df_pt_merged[f'{feature}_false'][-50:], color='blue')
    inset_ax.plot(df_pt_merged['iteration'][-50:], df_pt_merged[f'{feature}_true'][-50:], color='orange')
    inset_ax.set_xticks([])

plt.tight_layout()
plt.savefig(f'RQ4.png', dpi=300)
