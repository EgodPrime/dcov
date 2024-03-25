results = dict()
import oneflow
import numpy as np

oneflow.device("cpu")
arg_0_0 = 2
arg_0_1 = 3
arg_0 = [arg_0_0,arg_0_1,]
results["res"] = oneflow.empty(arg_0,)
