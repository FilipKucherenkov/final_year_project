from structures.job import Job


class Timeslot:
    """
    Simple class to represent each timeslot from our time horizon (e.g [0,1], [1,2]). Each
    timeslot has a start time, end time, capacity for number of jobs that can be scheduled
    within it and a list of jobs containing the scheduled jobs.

    Note: A timeslot is active (open) if it has at lest one scheduled job in it.

    Note: The purpose of this class is to only assist with implementing the greedy algorithms
    Not the optimisation models.
    """
    start_time: int
    end_time: int
    capacity: int
    jobs: list[Job]
    is_active: bool

    def __init__(self, start_time: int, end_time: int, g: int):
        self.start_time = start_time
        self.end_time = end_time
        self.capacity = g
        self.is_active = True

    def __str__(self):
        return f"[{self.start_time},{self.end_time}]"

    def is_full(self) -> bool:
        return len(self.jobs) == self.capacity

    def add_job(self, job: Job):
        self.jobs.append(job)
    def is_timeslot_within_job_window(self, job: Job):
        # A job j is said to be live at slot t if t ∈ [r j , d j ]
        return job.release_time <= self.start_time <= job.deadline
