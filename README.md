# Algorithms and Optimization models for Active Time Scheduling (Getting Started).

### Generating A Problem Instance (Guide)
To facilitate the generation of problem instances, we provide the following three separate scripts under `input_generation/scripts`:
- `generate_custom_instance.py`: Generates custom problem instances suitable for test- ing small-scale problems.
- `generate_random_instance.py`: Generates random problem instances suitable for ana- lyzing larger-scale problems.
- `generate_dataset`: Generates datasets suitable for analyzing a larger number of problem instances of varying sizes.

Example commands:
- Generate a custom instance with 100 time slots, 2 jobs and a capacity limit 50. 
```
python3 -m input_generation.scripts.generate_custom_instance --name "user_guide_example_1" --T 100 --G 50 --jobs "0-7-5, 0-3-1"

```
- Generate a random instance with 100 time slots, 10 jobs and a capacity limit 2. (Note: It does not guarantee feasiblity on purpose.)
```
python3 -m input_generation.scripts.generate_random_instance --name "user_guide_example_2" --T 100 --G 2 --J 10

```
- Generate datasets with feasible instances. (Please note that the script for generating datasets may not be user-friendly and could require manual adjustments for specific parameters to generate datasets with diverse problem instances, as we did.)
```
python3 -m input_generation.scripts.generate_dataset --T_range "25, 50, 100, 150, 250, 500" --P "T" --name "test"
```

The scripts additionally provide more information with the -h (or --help) flag enabled.




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
