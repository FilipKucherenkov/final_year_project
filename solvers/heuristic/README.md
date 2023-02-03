## Simple Greedy Heuristics not respecting the batch capacity

Folder contains implementations for the following methods:
- `earliest_released_first.py`: Greedy algorithm which schedules each job at its release time.
- `erf_with_back_filling.py`: Greedy algorithm which is based on Earliest-released-first strategy with 2 heuristics tog guide its decisions:
    - Heuristic 1: Sort jobs based on h(j) = (j.deadline - j.release_time) / j.processing_time
    - Heuristic 2: Prioritise scheduling at the most dense intervals 