## Integer programming formulation for the Active time problem
#### **Paper:** *LP rounding and combinatorial algorithms for minimizing active and busy time, 2017*
#### **Authors:** *Jessica Chang, Samir Khuller, Koyel Mukherjee*


Folder contains implementations for the following methods:
- `active_time_ip.py`: A method for constructing and solving a Pyomo optimization model based on the Integer programming formulation from the paper (with slight modifications). 
- `unbounded_active_time_ip.py`: A method for constructing and solving a Pyomo Optimization model  based on the Integer programming formulation from the paper. Note: This formulation is different as it allows for assigning an unbounded number of jobs to be processed in parallel and aims to additionally minimize that number.