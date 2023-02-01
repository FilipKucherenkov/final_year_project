# Robustness analysis of Active Time Scheduling problem.
### Getting started

### Input Generation
#### 1. Custom instances
To generate a json file with a custom problem instance use the `generate_custom_instance.py` script from the `input_generation` package. The script requires 3 separate arguments:
 - **name:** give a name to your instance file
 - **T:** number of timeslots in the problem instance.
 - **G:** number of jobs that can be scheduled in parallel.
 - **jobs:** The different properties of each job as a string of comma-separated values: `"job_release-job_deadline-job_processing, ..."`
 - For an example consider the following command:
```commandline
python3 -m input_generation.scripts.generate_custom_instance --name "test" --T 100 --G 50 --jobs "0-7-5, 0-3-1"
```
#### 2. Random instance
#### 3. Dataset with random instances
#### 4. Dataset Perturbator


### Solving a problem instance
Users can utilize the implemented solvers using the `solve_problem_instance.py` script, providing the correct arguments. The script requires the following 3 arguments:
 - **file:** This is the path from the top-level directory to a json file which contains a problem instance.
 - **algorithm:** Optionally specify one of the implemented algorithms. If no argument is provided, the script will use the Integer Programming model by default
 - **solver_type:** Optionally specify a solver on your system. If no argument is provided, the script will use the CPLEX commercial optimization solver by default.
```
python3 -m solve_problem_instance --file "data/custom_instances/test.json" --algorithm "Greedy-local-search: Pyomo"
```

### Recording performance & Analysing results
