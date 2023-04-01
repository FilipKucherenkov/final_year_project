## Scripts for Recording Results

### Folder contains 4 scripts that are used for recording various results:
#### `record_solver_performance.py`: 
- Script for recording objective and runtime performance of a method on a specified dataset. 
- Results are stored under `data/results/runtime` and `data/results/objective`
- Example command or alternatively specify --help for the full list of available options:
```
python3 -m stats.scripts.record_solver_performance --file "data/feasible_sets/instances_with_changes_in_batch_size_set.json" --analysis_type "runtime" --algorithm "Greedy-local-search: CPLEX Re-optimization"
```

#### `record_objective_deviation.py`:
- Script for recording the objective performance of a method on a nominal instance and all of corresponding perturbed instances. 
- Results are stored under `data/results/perturbation`
- Example command or alternatively specify --help for the full list of available options:
```
python3 -m stats.scripts.record_objective_deviation --method "Greedy-local-search: CPLEX Re-optimization" --nominal_id f0870c8e-6fbd-43cb-8a91-a33a0724aca0
```

#### `analyse_dataset.py`: 
- Script for producing statistics for each of the generated datasets.
- Results are stored under `data/dataset_stats`
- Example command or alternatively specify --help for the full list of available options:
```
python3 -m stats.scripts.analyse_dataset --file "data/feasible_sets/dataset_6.json"
```