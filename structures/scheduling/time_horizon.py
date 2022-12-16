import math

from structures.scheduling.timeslot import Timeslot


class TimeHorizon:
    """
    Simple class to represent the time horizon in our problem instance. The time horizon contains a
    list of timeslots - time_slots and slot_capacity - number of jobs that can be scheduled in parallel
    within each timeslot.
    """

    def __init__(self, t: int, g: int):
        self.slot_capacity: int = g
        self.t: int = t
        prev: int = 0
        new_time_slots: list[Timeslot] = []
        for i in range(1, t + 1):
            new_time_slots.append(Timeslot(prev, g))
            prev = i
        self.time_slots: list[Timeslot] = new_time_slots

    def __str__(self):
        horizon: str = f"Time Horizon:"
        for i in range(0, len(self.time_slots)):
            horizon = horizon + f" Timeslot {i}: {self.time_slots[i]} {'A' if self.time_slots[i].is_active else 'N'}"
        return horizon
