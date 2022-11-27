from structures.scheduling.job import Job
from structures.scheduling.timeslot import Timeslot


class Schedule:
    """
    Schedule class to assist with saving solutions from scheduling algorithms.
    A schedule is infeasible if it does not satisfy the constraints of the Active Time problem.
    """

    def __init__(self, jobs: list[Job], timeslots: list[Timeslot], is_feasible: bool):
        self.is_feasible = is_feasible
        self.timeslots = timeslots[:] if len(timeslots) > 0 else []
        self.jobs = jobs[:] if len(jobs) > 0 else []

    # Calculate the number of active slots in this schedule
    def calculate_active_time(self):
        count: int = 0
        for t in self.timeslots:
            if t.is_active:
                count = count + 1
        return count

    # Given a job number (e.g. 0, 1, 2) and a timeslot's start time
    # schedule that job at the timeslot.
    def schedule_job(self, job_number: int, timeslot_start):
        job_to_schedule = self.jobs[job_number]
        for timeslot in self.timeslots:
            if timeslot.start_time == timeslot_start:
                timeslot.add_job(job_to_schedule)
                timeslot.is_active = True

    # Print extended information about solution
    # (e.g. at which timeslot was each job scheduled.
    def print_schedule_info(self):
        print(f"Total active time: {self.calculate_active_time()}")
        print(f"Is schedule feasible? {'Yes' if self.is_feasible else 'No'}")
        # for timeslot in self.timeslots:
        #     if len(timeslot.jobs) > 0:
        #         print(f"Timeslot {timeslot.start_time}, scheduled jobs:")
        #         for job in timeslot.jobs:
        #             print(f"Job {job.number}, r:{job.release_time} d:{job.deadline} p:{job.processing_time}")
