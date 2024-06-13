## FreeFuzz+DCOV

> FreeFuzz supports TensorFlow 2.11.0 and PyTorch 2.1.0
> https://github.com/ise-uiuc/FreeFuzz

### Test Configuration

FreeFuzz contains documents for 1700+ APIs in TensorFlow and 400+ APIs in PyTorch, it's workload of fuzzing can be configured by parameter `each_api_run_times`. We configure `each_api_run_times` to 10, and the entire testing can be finished in 12 hours.

### Coverage curve of TensorFlow 

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_freefuzz_tf.png" alt="Curve">

log file is at [here](./run_freefuzz_tf.log)

### Coverage curve of PyTorch

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_freefuzz_pt.png" alt="Curve">

log file is at [here](./run_freefuzz_pt.log)

### Description

FreeFuzz is an API fuzzer that pre-collects a large number of API specifications for TensorFlow and PyTorch, distinguishing them by API names. The horizontal axis of the coverage curve chart represents the ID of APIs, with its growth indicating the cumulative testing of different APIs. The vertical axis is the basic block coverage count. These curves reveal the process in which FreeFuzz achieves an increasingly higher total coverage as it tests more different APIs for TensorFlow and PyTorch.

## COMET+DCOV

> COMET generates test cases for several DL frameworks at the same time, but utlizes only one DL framework as the back end to evaluate.
>
> Note: The Github repo of COMET is closed now, so its latest source code is not available. As a consequence, we have only the old version of COMET. However, this version of COMET supports Python 3.7 for TensorFlow 2.9 and Python 3.6 for PyTroch 1.10.0. But DCOV requires at least Python3.8 to finish the Python instrumentation. Thus we only collect C coverage for COMET.

### Test Configuration

COMET offers a parameter named `max_iter` to control the total number of test iterations. Considering that model-level testing is pretty slow, we configure `max_iter` to 100, which wll cost about 4 hours to finish the testing.

### Coverage curve of TensorFlow 

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_comet_tf.png" alt="Curve">

log file is at [here](./run_comet_tf.log)

### Coverage curve of PyTorch

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_comet_pt.png" alt="Curve">

log file is at [here](./run_comet_pt.log)

### Description

COMET is an archetecture level fuzzer that perfrom neural network model and layer mutation to generate test cases.  The horizontal axis of the coverage curve chart represents the test iterations (a whole process of obtaining a legal new model from an original model with several times of failures). The vertical axis is the basic block coverage count. These curves reveal the process in which COMET achieves an increasingly higher total coverage as it generates more different models for TensorFlow and PyTorch.

## Comparaison

We notice that the C coverage curve of COMET grows simlilarly to that of FreeFuzz. However, we observe the below differences:

1.  For TensorFlow, the curve of COMET starts from a higher point (34124) than that of FreeFuzz (14645). 

2.  For PyTorch, the curve of COMET starts from a lower point (8218) than that of FreeFuzz (13554).

The first reason for the differences is the DL framework version difference between COMET and FreeFuzz.

The second reason can be attributed to the fact that COMET is a model-level fuzzer while FreeFuzz is an API-level fuzzer. Executing a model and executing an API call require the different components in DL frameworks.