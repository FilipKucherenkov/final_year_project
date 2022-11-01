import math

from structures.timeslot import Timeslot


class TimeHorizon:
    """
    Simple class to represent the time horizon in our problem instance. The time horizon contains a
    list of timeslots - time_slots and slot_capacity - number of jobs that can be scheduled in parallel
    within each timeslot.
    """
    time_slots: list[Timeslot] = []
    slot_capacity: int

    def __init__(self, t: int, g: int = math.inf):
        self.slot_capacity = g
        prev: int = 0
        for i in range(1, t + 1):
            self.time_slots.append(Timeslot(prev, i, g))
            prev = i

    def __str__(self):
        horizon: str = f"Time Horizon:"
        for i in range(0, len(self.time_slots)):
            horizon = horizon + f" Timeslot {i}: {self.time_slots[i]}"
        return horizon
