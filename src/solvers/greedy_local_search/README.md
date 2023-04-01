## Greedy local search algorithm for solving the Active time problem.
#### **Paper:** *Brief Announcement: A Greedy 2 Approximation for the Active Time Problem, 2018*
#### **Authors:** *Saurabh Kumar & Samir Khuller*
 
- **Algorithm:** All time slots are assumed to be open initially. Consider time slots from left to right (i.e in increasing
    order). At a given time slot, close the slot and check if a feasible schedule exists (via Max-flow computation) in the open slots. If so,
    leave the slot closed, otherwise, open it again. Continue to the next slot. 


Folder contains the following implementations of the algorithm.
- `greedy_local_search.py`: Our initial implementation which uses a Pyomo model for computing Max-flow as a subroutine.
- `greedy_local_search_with_cplex.py`: The change in this version is that we instead use a CPLEX model for computing the Max-flow. This change has significantly improved the runtime of the algorithm.
- `greedy_local_search_with_cplex_v2.py`: An alternative approach to the one above where the main difference is in specifying the objective when computing Max-flow (V1 maximises flow outflow from source node, V2 maximises inflow to sink node).
- `greedy_local_search_cplex_with_reopt.py`: This version of the algorithm mitigates the impact of computing Max-flow several times. It utilises the "modify and reoptimize" feature provided by the CPLEX python API. The main idea is build a single CPLEX model and incrementally change it by adding and removing constraints. Hence, allowing us to compute much larger problem instances than the previously described approaches.  
(Check for more information: https://perso.ensta-paris.fr/~diam/ro/online/cplex/cplex1271/CPLEX/GettingStarted/topics/tutorials/Python/modify_reopt.html). 




