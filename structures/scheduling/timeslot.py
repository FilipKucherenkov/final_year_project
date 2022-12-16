from structures.scheduling.job import Job


class Timeslot:
    """
    Simple class to represent each timeslot from our time horizon (e.g [0,1], [1,2]). Each
    timeslot has a start time, end time, capacity for number of jobs that can be scheduled
    within it and a list of jobs containing the scheduled jobs.

    Note: A timeslot is active (open) if it has at lest one scheduled job in it.

    Note: The purpose of this class is to only assist with implementing the greedy_algorithms algorithms
    Not the optimisation models.
    """

    def __init__(self, start_time: int, g: int):
        self.start_time: int = start_time
        self.capacity: int = g
        self.is_active: bool = False
        self.is_open: bool = True
        self.jobs: list[Job] = []

    def __str__(self):
        return f"{self.start_time}"

    def is_full(self) -> bool:
        return len(self.jobs) == self.capacity

    def add_job(self, job: Job):
        self.jobs.append(job)

    def is_timeslot_within_job_window(self, job: Job):
        # A job j is said to be live at slot t if t ∈ [r j , d j )
        return job.release_time <= self.start_time < job.deadline
