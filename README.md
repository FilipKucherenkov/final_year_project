# Algorithms and Optimization models for Active Time Scheduling (Getting Started).

### Input Generation (Guide)
#### 1. How to generate a custom problem instance:
For generating custom problem instances use the `generate_custom_instance.py` script from the `input_generation` package. The script requires 3 arguments:
 - **name:** Specify a name for the generate instance
 - **T:** Specify the number of timeslots in the problem instance.
 - **G:** Specify the number of jobs that can be scheduled in parallel (capacity limit).
 - **jobs:** Specify the different properties of each job as a string of comma-separated values: `"job_release-job_deadline-job_processing, ..."`
 - Example command:
```commandline
python3 -m input_generation.scripts.generate_custom_instance --name "test" --T 100 --G 50 --jobs "0-7-5, 0-3-1"
```
#### 2. How to generate a random problem instance:
#### 3. How to generate a dataset containing random problem instances:
#### 4. How to generate a perturbed problem instance:


### Solving problem instances

#### 1. How to solve a problem instance using the Deterministic Methods:
For solving a specific problem instance using the deterministic methods use the `solve_problem_instance.py` script. The script requires 3 arguments:
 - **file:** Specify path from top-level directory to a json file containing a problem instance.
 - **algorithm:** Optionally specify one of the implemented algorithms. If no argument is provided, the script will use the Integer Programming model by default
 - **solver_type:** Optionally specify a solver on your system. If no argument is provided, the script will use the CPLEX commercial optimization solver by default.
```
python3 -m solve_problem_instance --file "data/custom_instances/test.json" --algorithm "Greedy-local-search: Pyomo"
```
#### 2. How to solve a perturbed instance using the Recovery Model:
For solving a specific perturbed instance using the recovery model use the `<add_script>` script. 


### Performance monitoring
Scripts for monitoring performance are provided under `stats/scripts/` directory. The folder contains an additional `README.md` file with further instructions. We provide scripts to measure the following metrics.
- `record_solver_performance.py`: used for measuring performance of the deterministic methods (runtime, objective value):
- `record_objective_deviation.py`: used for measuring deviation in the obtained objective value from deterministic methods before and after uncertainty realisation.
- `record_recovery.py`: used for measuring performance (objective, runtime) of the recovery model on perturbed instances and comparing it with the deterministic IP Model.

### Other:
The `utils/` folder contains helper functions we used throughout the project:
- `utils/file_writers.py`: contains helper functions for writing results to files.
- `utils/parsing.py`: contains helper functions used for parsing files to python objects.
- `utils/performance_monitors.py`: contains helper functions used for recording performance.
- `utils/plot_functions.py`: contains helper functions used for plotting specific results.
- `utils/plot_producer.py`: helper class assisting when plotting results. 
- `utils/statistics.py`: contains functions for computing statistical results.
