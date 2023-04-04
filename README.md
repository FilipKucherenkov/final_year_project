# Algorithms and Optimization models for Active Time Scheduling (Getting Started)
### 1. Tools and Technologies
Our project primarily utilizes Python, which offers a rich set of libraries and tools for optimization modelling and data analysis. To implement our models, we leverage [Pyomo](https://pyomo.readthedocs.io/en/stable/), a Python-based optimization modelling language that allows flexible translation of algebraic notations to code. Pyomo offers a robust way to develop linear and integer programming models. It has the advantage over other modelling languages, such as GAMS or AMPL, as its modelling objects are embedded within Python, providing access to a rich set of supporting libraries. Additionally, Pyomo can utilize commercial optimization solvers such as [CPLEX](https://www.ibm.com/docs/en/icos/12.8.0.0?topic=cplex-users-manual) and [Gurobi](https://www.gurobi.com/documentation/10.0/refman/index.html), which are available under free academic licensing to solve implemented models.

On the other hand, it should be noted that Pyomo may have certain limitations, including performance and supported functionalities. As a result, using a solver's core API directly can be more efficient in many situations, as it provides additional functionalities to the user. For instance, we utilize CPLEX's core [Python API](https://home.engineering.iastate.edu/~jdm/ee458/CPLEX-UsersManual2015.pdf) to implement the Greedy Local Search with re-opt, taking advantage of its ["modify and re-optimize"](https://www.ibm.com/docs/en/icos/12.9.0?topic=tutorial-modifying-re-optimizing) feature to mitigate the impact of multiple max-flow computations. This method allows us to make incremental changes to the model and re-optimize the solution without solving the entire model again.

To manipulate and analyze the solver results, we use [Pandas](https://pandas.pydata.org/docs/), an open-source library for data manipulation and analysis. For visualizing the results, we utilize [Seaborn](https://seaborn.pydata.org), which is built on top of [Matplotlib](https://matplotlib.org) - another popular open-source Python library used for data visualization. Seaborn offers additional visualization capabilities that simplify the creation of complex visualizations.

### 2. File Structure
- `data/` directory contains the `.json` files that store the results of our evaluation, such as plots, statistics, and numerical results.
- `input_generation/` directory contains scripts and functionality related to synthetic data generation and perturbations.
- `problem_classes/` directory contains the Python classes we used to assist with data representation.
- `solvers/` directory contains all the methods we implemented, including the IP Recovery model, Capacity Search method, and the integration between GLS and Capacity Search.
- `stats/` and `utils/` directories contain helper functions and classes that we used as part of our analysis and implementation.
\end{itemize}

### 3. Generating A Problem Instance (Guide)
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

### 4. Perturbing A Problem Instance
To introduce disturbances into problem instances, we offer a separate script, `perturb_instance.py`, which utilizes the `perturbator.py` class. Please note that in order to perturb a problem instance, its JSON file must be located in the `data/nominal_instances/` directory. The perturbed instance file will be generated in a separate directory with a name corresponding to the ID of the nominal instance, located in `data/perturbed_instances/<nominal_instance_id>/`. For further information enable the `--help` (or `-h`) flag. 

Example command:
```
python3 -m input_generation.scripts.perturb_instance --instance_file user_guide_example_4 --gamma 20 --epsilon 20
```

<img width="1376" alt="Screen Shot 2023-04-04 at 18 58 20" src="https://user-images.githubusercontent.com/72323426/229878487-0f779c80-9593-45db-8e2c-f6b89daabc22.png">


### 4. Solving Instances Using Deterministic Methods
To solve problem instances using the implemented deterministic methods, we provide the `solve_problem_instance.py` script, which utilizes the `solver_handler.py` module. The solution is stored in a 2-dimensional matrix where the rows represent jobs, and the columns represent time slots. For ease of use, we display this information in the terminal, along with the active time, the number of changed variables, and the batch violation. For further information enable the `--help` (or `-h`) flag. 

Example command for solving a custom instance using the GLS method (Pyomo implementation):
```
python3 -m solve_problem_instance --file "data/custom_instances/test.json" --algorithm "Greedy-local-search: Pyomo"
```
<img width="1385" alt="Screen Shot 2023-04-01 at 17 29 24" src="https://user-images.githubusercontent.com/72323426/229880246-75cbf4c7-e6f7-4f98-bbce-b6604eab7ce0.png">

### 5. Recovering Schedule From Disturbances
For demonstration purposes, we provide the `recover_schedule.py` script, which utilizes both the `solver_handler.py` and `recovery_handler.py` modules. This script first solves the specified nominal scenario using the deterministic IP model, then uses the solution to solve the true scenario using the recovery IP model with provided weights for the two cost functions and an upper bound on the number of perturbed jobs. or further information enable the `--help` (or `-h`) flag. 

Example command for recovering a schedule:
```
python3 -m recover_schedule --nominal_instance data/nominal_instances/runtime_test.json --perturbed_instance data/perturbed_instances/35fa8883-f4fa-4133-9d19-958bceed0b8f/e2b4af16-7c4c-4433-abaa-3a65659da3e1.json --v1 1 --v2 1 --gamma 25
```
<img width="1636" alt="Screen Shot 2023-04-01 at 19 38 43" src="https://user-images.githubusercontent.com/72323426/229880108-7abf54f4-a2e4-4286-acdc-c76058cc2e1c.png">


### 6. Performance monitoring
Scripts for monitoring performance are provided under `stats/scripts/` directory. The folder contains an additional `README.md` file with further instructions. We provide scripts to measure the following metrics.
- `record_solver_performance.py`: used for measuring performance of the deterministic methods (runtime, objective value):
- `record_objective_deviation.py`: used for measuring deviation in the obtained objective value from deterministic methods before and after uncertainty realisation.
- `record_recovery.py`: used for measuring performance (objective, runtime) of the recovery model on perturbed instances and comparing it with the deterministic IP Model.

### 7. Additional Information:
The `utils/` folder contains helper functions we used throughout the project:
- `utils/file_writers.py`: contains helper functions for writing results to files.
- `utils/parsing.py`: contains helper functions used for parsing files to python objects.
- `utils/performance_monitors.py`: contains helper functions used for recording performance.
- `utils/plot_functions.py`: contains helper functions used for plotting specific results.
- `utils/plot_producer.py`: helper class assisting when plotting results. 
- `utils/statistics.py`: contains functions for computing statistical results.
