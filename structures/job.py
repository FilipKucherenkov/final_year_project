class Job:
    """
    Simple class to represent a Job. A job has a number (e.g. Job 1), processing time, release time and deadline.
    """
    number: int
    processing_time: int
    release_time: int
    deadline: int

    def __init__(self, number: int):
        self.number = number

    def get_properties(self):
        return f""" Job {self.number}:[R:{self.release_time}, D:{self.deadline}, P:{self.processing_time}]"""

