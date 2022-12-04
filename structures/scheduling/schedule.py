from structures.scheduling.job import Job
from structures.scheduling.timeslot import Timeslot


class Schedule:
    """
    Schedule class to assist with saving solutions from scheduling algorithms.
    A schedule is infeasible if it does not satisfy the constraints of the Active Time problem.
    """

    def __init__(self, is_feasible: bool, job_to_timeslot_mapping):
        self.is_feasible = is_feasible
        self.schedule = job_to_timeslot_mapping

    # Calculate the number of active slots in this schedule
    def calculate_active_time(self):
        count = 0
        used = {}
        for job, slot in self.schedule:
            if slot not in used or not used[slot]:
                used[slot] = True
                count = count + 1
        return count

    # Print extended information about solution
    # (e.g. at which timeslot was each job scheduled.
    def print_schedule_info(self):
        print(f"Total active time: {self.calculate_active_time()}")
        print(f"Is schedule feasible? {'Yes' if self.is_feasible else 'No'}")
        for placement in self.schedule:
          print(placement)
