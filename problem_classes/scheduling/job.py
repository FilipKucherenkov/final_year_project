class Job:
    """
    Class to represent a Job. A job has a number (e.g. Job 1), processing time, release time and deadline.
    """
    number: int
    processing_time: int
    release_time: int
    deadline: int

    def __init__(self, number: int, release_time: int = -1, deadline: int = -1, processing_time: int = -1):
        self.number = number
        self.release_time = release_time
        self.deadline = deadline
        self.processing_time = processing_time

    def get_properties(self):
        return f""" Job {self.number}:[R:{self.release_time}, D:{self.deadline}, P:{self.processing_time}]"""

