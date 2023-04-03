# Nominal instances (Guide)
#### Note: Folder contains some of the nominal instances we used as part of our analysis. Specifically, we used the Perturbator to introduce disturbances. The corresponding perturbed instances are stored under `data/perturbed_instances/` in separate folders where each folder corresponds to a different nominal instances.  


#### runtime_test.json Gamma = 25, epsilon 0.75, v1 = 1, v2 = 1
- Recovery model: 0.06112134033333335 secs
- Expected active time: 15
- Recovered active time: 16
- Number of changes: 17.0

#### runtime_test.json Gamma = 25, epsilon 0.75, v1 = 0, v2 = 1
- Deterministic model: 0.05462324733333338 secs
- Recovery model: 0.060519272666666644 secs
- Expected active time: 15
- Recovered active time: 14
- Number of changes: 77.0

#### runtime_test.json Gamma = 25, epsilon 0.75, v1 = 1, v2 = 0
- Deterministic model: 0.05248085199999997 secs
- Recovery model: 0.05999835566666667 secs
- Expected active time: 15
- Recovered active time: 18
- Number of changes: 17.0

#### runtime_test.json Gamma = 25, epsilon 0.75, v1 = 0.5, v2 = {1,2}
- Deterministic model: 0.0515835183333333 secs
- Recovery model: 0.06575384233333333 secs
- Expected active time: 15
- Recovered active time: 16
- Number of changes: 17.0

#### runtime_test.json Gamma = 25, epsilon 0.75, v1 = 0.5, v2 = {3,4}
- Deterministic model: 0.052420678000000054 secs
- Recovery model: 0.07125773033333334 secs
- Expected active time: 15
- Recovered active time: 15
- Number of changes: 23.0

#### runtime_test.json Gamma = 25, epsilon 0.75, v1 = 0.5, v2 = {5,6,7,8,9,10}[No effect after 5]
- Deterministic model: 0.05201900800000003 secs
- Recovery model: 0.060758874666666664 secs
- Expected active time: 15
- Recovered active time: 14
- Number of changes: 33.0
-------------------------------------------------------------------------


#### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 1, v2 = 1
- Deterministic model: 0.3157926933333333 secs
- Recovery model: 0.2173655263333334 secs
- Expected active time: 17
- Recovered active time: 17
- Number of changes: 52.0


#### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 0, v2 = 1
- Deterministic model: 0.31604017766666664 secs
- Recovery model: 0.31607758699999994 secs
- Expected active time: 17
- Recovered active time: 13
- Number of changes: 212.0

#### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 1, v2 = 0
- Deterministic model: 0.2774703006666668 secs
- Recovery model: 0.20539668700000005 secs
- Expected active time: 17
- Recovered active time: 20
- Number of changes: 52.0

#### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 0.5, v2 = 1
- Deterministic model: 0.27523165866666677 secs
- Recovery model: 0.21703122133333333 secs
- Expected active time: 17
- Recovered active time: 17
- Number of changes: 52.0

### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 0.4, v2 = 3
- Deterministic model: 0.2739589416666665 secs
- Recovery model: 0.21541556266666673 secs
- Expected active time: 17
- Recovered active time: 15
- Number of changes: 64.0

#### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 0.5, v2 = 3
- Deterministic model: 0.2734920463333334 secs
- Recovery model: 0.21602357333333325 secs
- Expected active time: 17
- Recovered active time: 16
- Number of changes: 58.0

### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 0.5, v2 = 4
- Deterministic model: 0.27622195166666685 secs
- Recovery model: 0.21819781500000004 secs
- Expected active time: 17
- Recovered active time: 15
- Number of changes: 64.0

### runtime_test_2.json Gamma = 50, epsilon 0.75, v1 = 0.5, v2 = 5
- Deterministic model: 0.27486229366666654 secs
- Recovery model: 0.21347905999999997 secs
- Expected active time: 17
- Recovered active time: 14
- Number of changes: 72.0

-------------------------------------------------------------------------
#### runtime_test_3.json Gamma = 100, epsilon 0.75, v1 = 1, v2 = 1
- Deterministic model: 0.33285775133333334 secs
- Recovery model: 0.24926232133333345 secs
- Expected active time: 46
- Recovered active time: 22
- Number of changes: 229.0


#### runtime_test_3.json Gamma = 100, epsilon 0.75, v1 = 0, v2 = 1
- Deterministic model: 0.28139776199999983 secs
- Recovery model: 0.3553820466666666 secs
- Expected active time: 46
- Recovered active time: 13
- Number of changes: 303.0


#### runtime_test_3.json Gamma = 100, epsilon 0.75, v1 = 1, v2 = 0
- Deterministic model: 0.2808213256666668 secs
- Recovery model: 0.21360410066666669 secs
- Expected active time: 46
- Recovered active time: 36
- Number of changes: 229.0



#### runtime_test_3.json Gamma = 100, epsilon 0.75, v1 = 0.5, v2 = 1
- Deterministic model: 0.2800307803333337 secs
- Recovery model: 0.22598923666666662 secs
- Expected active time: 46
- Recovered active time: 20
- Number of changes: 233.0

#### runtime_test_3.json Gamma = 100, epsilon 0.75, v1 = 0.5, v2 = 2
- Deterministic model: 0.2845401746666667 secs
- Recovery model: 0.22205588299999976 secs
- Expected active time: 46
- Recovered active time: 14
- Number of changes: 253.0

### runtime_test_3.json Gamma = 100, epsilon 0.75, v1 = 0.5, v2 = {3,4}[No effect after 3]
- Deterministic model: 0.31073913933333347 secs
- Recovery model: 0.2877138763333331 secs
- Expected active time: 46
- Recovered active time: 13
- Number of changes: 257.0


-------------------------------------------------------------------------
#### runtime_test_4.json Gamma = 150, epsilon 0.75, v1 = 1, v2 = 1
- Deterministic model: 1.454595693666666 secs
- Recovery model: 1.9871481623333327 secs
- Expected active time: 79
- Recovered active time: 117
- Number of changes: 750.0


#### runtime_test_4.json Gamma = 150, epsilon 0.75, v1 = 0, v2 = 1
- Deterministic model: 1.444215048666668 secs
- Recovery model: 1.8408730420000008 secs
- Expected active time: 79
- Recovered active time: 115
- Number of changes: 2858.0


#### runtime_test_4.json Gamma = 150, epsilon 0.75, v1 = 1, v2 = 0
- Deterministic model: 1.464520422333332 secs
- Recovery model: 1.9546178716666656 secs
- Expected active time: 79
- Recovered active time: 134
- Number of changes: 750.0

#### runtime_test_4.json Gamma = 150, epsilon 0.75, v1 = 0.5, v2 = 1
- Deterministic model: 1.7245761423333335 secs
- Recovery model: 2.1747919019999977 secs
- Expected active time: 79
- Recovered active time: 117
- Number of changes: 750.0

#### runtime_test_4.json Gamma = 150, epsilon 0.75, v1 = 0.5, v2 = 1
- Deterministic model: 1.7245761423333335 secs
- Recovery model: 2.1747919019999977 secs
- Expected active time: 79
- Recovered active time: 117
- Number of changes: 750.0



-------------------------------------------------------------------------

#### runtime_test_5.json Gamma = 250, epsilon 0.75, v1 = 1, v2 = 1
2023-04-02 23:29:58,377:INFO:Deterministic model: 5.753649492666663 secs
2023-04-02 23:29:58,377:INFO:Recovery model: 6.292057436666663 secs

#### runtime_test_5.json Gamma = 150, epsilon 0.75, v1 = 0, v2 = 1
2023-04-02 23:49:41,555:INFO:Deterministic model: 5.101130504666666 secs
2023-04-02 23:49:41,555:INFO:Recovery model: 6.718358687000001 secs

#### runtime_test_5.json Gamma = 150, epsilon 0.75, v1 = 1, v2 = 0
2023-04-02 23:34:39,975:INFO:Deterministic model: 5.770935393666671 secs
2023-04-02 23:34:39,975:INFO:Recovery model: 5.965921825333339 secs

#### runtime_test_5.json Gamma = 150, epsilon 0.75, v1 = 0.1, v2 = 2
2023-04-02 23:55:28,059:INFO:Deterministic model: 5.002375481333341 secs
2023-04-02 23:55:28,059:INFO:Recovery model: 5.940519441333332 secs




