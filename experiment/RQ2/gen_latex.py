template_pre = r"""\begin{tabular}{lrrrrrrrrrrrrrrrr} \hline \multicolumn{1}{c}{DL} & \multicolumn{1}{c}{No Cov} & 
\multicolumn{3}{c}{Coverage.py} & \multicolumn{3}{c}{SlipCover} & \multicolumn{3}{c}{DCOV-Python} & \multicolumn{3}{
c}{DCOV-C} & \multicolumn{3}{c}{DCOV} \\ \cline{2-17} \multicolumn{1}{c}{Framework} & \multicolumn{1}{c}{E.T.\tnote{
1}} & \multicolumn{1}{c}{E.T.} & \multicolumn{1}{c}{A.T.\tnote{2}} & \multicolumn{1}{c}{T.T.\tnote{3}} & 
\multicolumn{1}{c}{E.T.} & \multicolumn{1}{c}{A.T.} & \multicolumn{1}{c}{T.T.} & \multicolumn{1}{c}{E.T.} & 
\multicolumn{1}{c}{A.T.} & \multicolumn{1}{c}{T.T.} & \multicolumn{1}{c}{E.T.} & \multicolumn{1}{c}{A.T.} & 
\multicolumn{1}{c}{T.T.} & \multicolumn{1}{c}{E.T.} & \multicolumn{1}{c}{A.T.} & \multicolumn{1}{c}{T.T.} \\
\hline"""

template_post = r"""
\bottomrule
\end{tabular}
"""

DLF_MAP = {
    'tensorflow': "TensorFlow",
    'torch': "PyTorch",
    'paddle': "PaddlePaddle"
}

num_scripts = 100
num_repeat = 100
divider = num_scripts * num_repeat


def gen():
    results_file_path = './results.txt'
    data = {}
    with open(results_file_path, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            tokens = line.strip().split(',')
            libname = tokens[0]
            mode = tokens[1]
            if libname not in data:
                data[libname] = {}
            dlf_data = data[libname]
            dlf_data[mode] = tokens[2:]  # E.T.,A.T.,T.T.

    res = template_pre + '\n'
    for dlf in ['tensorflow', 'torch', 'paddle']:
        res += DLF_MAP[dlf] + ' &'
        datas = [data[dlf]['base'][-1]]
        for mode in ['coverage.py', 'slipcover', 'dcov-python', 'dcov-c', 'dcov']:
            datas += data[dlf][mode]
        datas_t = [float(x) / divider for x in datas]
        datas = [f"{x:.2f}" for x in datas_t]
        res += ' & '.join(datas)
        res += ' \\\\\n'

    res += template_post
    print(res)


if __name__ == '__main__':
    gen()
