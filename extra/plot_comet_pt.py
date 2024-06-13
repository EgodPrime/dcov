import matplotlib.pyplot as plt

file_path = './run_comet_pt.log'

c_covs=[]

def get_cov_num(t:str):
    return int(t.split('=')[1].strip())

f = open(file_path, 'r')
lines = f.readlines()
for line in lines:
    if 'coverage_c=' in line:
        c_cov = get_cov_num(line)
        c_covs.append(c_cov)

# 绘制曲线图
plt.figure(figsize=(10, 5))
plt.plot(c_covs, label='C  Coverage')
plt.xlabel('API Iteration')
plt.ylabel('Basic Code Block Coverage')
plt.title(f'Coverage Curve for COMET on PyTorch')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图像为 PNG 格式
plt.savefig('coverage_comet_pt.png', format='png')