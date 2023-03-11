class Schedule:
    """
    Schedule class to assist with saving solutions from scheduling algorithms.
    A schedule is infeasible if it does not satisfy the constraints of ATSP.
    """
    def __init__(self, is_feasible: bool, batch_limit: int, n, m):

        self.is_feasible: bool = is_feasible
        # solution is represented with a matrix j x t
        self.schedule = [[0 for i in range(0, m+1)] for j in range(0, n)]
        self.batch_limit = batch_limit

    # Calculate the number of active slots in this schedule
    def calculate_active_time(self):
        count = 0
        used = {}
        for job in range(0, len(self.schedule)):
            row = self.schedule[job]

            for timeslot in range(0, len(row)):
                if timeslot not in used and self.schedule[job][timeslot] == 1:
                    used[timeslot] = True
                    count = count + 1
        return count

    def calculate_batch_size(self):
        count = {}
        for job in range(0, len(self.schedule)):
            row = self.schedule[job]
            for timeslot in range(0, len(row)):
                if self.schedule[job][timeslot] == 1:
                    if timeslot in count:
                        count[timeslot] = count[timeslot] + 1
                    else:
                        count[timeslot] = 1

        batch_size = 0
        for timeslot, number_of_jobs in count.items():
            if number_of_jobs >= batch_size:
                batch_size = number_of_jobs
        return batch_size

    def add_mapping(self, job, timeslot):
        self.schedule[job][timeslot] = 1

    # Print extended information about solution
    # (e.g. at which timeslot was each job scheduled.
    def print_schedule_info(self):
        print(f"Total active time: {self.calculate_active_time()}")
        batch_size = self.calculate_batch_size()
        if batch_size > self.batch_limit:
            print(f"Batch violation: {batch_size - self.batch_limit}")
        else:
            print(f"Batch violation: {0}")

        print(f"Is schedule feasible? {'Yes' if self.is_feasible else 'No'}")
        print(f"Placements:")
        for job in range(0, len(self.schedule)):
            row = self.schedule[job]
            timeslots = ""
            for timeslot in range(0, len(row)):
                if self.schedule[job][timeslot] == 1:
                    timeslots = timeslots + f"{timeslot} "
            print(f"Job: {job} Timeslots: {timeslots}")
