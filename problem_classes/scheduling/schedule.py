from problem_classes.scheduling.job import Job
from problem_classes.scheduling.timeslot import Timeslot


class Schedule:
    """
    Schedule class to assist with saving solutions from scheduling algorithms.
    A schedule is infeasible if it does not satisfy the constraints of the Active Time problem.
    """

    def __init__(self, is_feasible: bool, job_to_timeslot_mapping: list[(str, str)], batch_size: int):
        self.is_feasible: bool = is_feasible
        self.schedule: list[(str, str)] = job_to_timeslot_mapping
        self.batch_size = batch_size

    # Calculate the number of active slots in this schedule
    def calculate_active_time(self):
        count = 0
        used = {}
        for job, slot in self.schedule:
            if slot not in used or not used[slot]:
                used[slot] = True
                count = count + 1
        return count

    # Calculate the batch utilization ratio of a schedule
    def calculate_batch_utilization_ratio(self):
        occurrences_map = {}

        for mapping in self.schedule:
            current_timeslot = mapping[1]
            # count number of jobs in each timeslot
            if current_timeslot in occurrences_map:
                occurrences_map[current_timeslot] = occurrences_map[current_timeslot] + 1
            else:
                occurrences_map[current_timeslot] = 1

        utilization_ration_map = {}

        for t, count in occurrences_map.items():
            # Calculate slot utilization in percentage
            utilization_ration_map[t] = count / self.batch_size * 100

        total_utilization = 0
        for t, util_perc in utilization_ration_map.items():
            total_utilization = total_utilization + util_perc
        return total_utilization / len(utilization_ration_map)

    # Print extended information about solution
    # (e.g. at which timeslot was each job scheduled.
    def print_schedule_info(self):
        print(f"Total active time: {self.calculate_active_time()}")
        print(f"Batch utilization: {self.calculate_batch_utilization_ratio()}%")
        print(f"Is schedule feasible? {'Yes' if self.is_feasible else 'No'}")
        for placement in self.schedule:
            print(placement)
