# Data sets for the Active time problem (Guide)
####  Note: The included json files contain multiple problem instances that are grouped based on changes in the parameters. This file contains information about the various data sets that are included. 

### 1. Data set contains 30 random problem instances with changes in the time horizon (5 instances per change): `dataset_1.json`
#### Parameters: 
- T = {25, 50, 100, 150, 250, 500}
- J = 100
- G = 20


### 2. Data set contains 30 random problem instances with proportional changes in J, T and G (5 instances per change): `dataset_2.json`
#### Note: Set contains large jobs e.g. (longer processing time)
#### Parameters: 
- T = {25, 50, 100, 150, 250, 500}
- J = {25, 50, 100, 150, 250, 500}
- G = 20 % of T 

### 3. Data set contains 20 random problem instances with changes in the time horizon (5 instances per change): `dataset_3.json`
#### Note: This set is used only to compare the 3 versions of the Greedy-local-search algorithm
#### Parameters: 
- T = {25, 50, 75, 100}
- J = 100
- G = 20

### 4. Data set contains 30 random problem instances with changes in the number of jobs (5 instances per change): `dataset_4.json`
#### Parameters: 
- T = 100
- J = {25,50,75,100,150,250}
- G = 5

### 5. Data set contains 30 random problem instances with changes in the batch size (5 instances per change): `dataset_5.json`
#### Parameters: 
- T = 100
- J = 100
- G = {5, 10, 25, 50, 100, 150}

###
