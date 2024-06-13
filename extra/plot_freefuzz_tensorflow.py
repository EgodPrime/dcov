import matplotlib.pyplot as plt

file_path = './run_freefuzz_tf.log'

py_covs = []
c_covs=[]

def get_cov_num(t:str):
    return int(t.split('=')[1].strip())

f = open(file_path, 'r')
lines = f.readlines()
for line in lines:
    if line.startswith('py_cov='):
        py_cov, c_cov = map(get_cov_num, line.split(','))
        py_covs.append(py_cov)
        c_covs.append(c_cov)

# 绘制曲线图
plt.figure(figsize=(10, 5))
plt.plot(py_covs, label='Python  Coverage')
plt.plot(c_covs, label='C  Coverage')
plt.xlabel('API Iteration')
plt.ylabel('Basic Code Block Coverage')
plt.title(f'Coverage Curve for FreeFuzz on TensorFlow')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图像为 PNG 格式
plt.savefig('coverage_freefuzz_tf.png', format='png')