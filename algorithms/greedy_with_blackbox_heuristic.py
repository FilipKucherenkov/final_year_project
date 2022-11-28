from input_generation.custom_instance import CustomInstance
from models.maxflow_with_parameters import solve_max_flow
from structures.helpers.generate_network import generate_network
from structures.scheduling.job import Job
from structures.scheduling.schedule import Schedule
from structures.scheduling.time_horizon import TimeHorizon


def greedy_with_blackbox_heuristic(instance):
    """
    All time slots are assumed to be open initially. Consider time slots from left to right (i.e in increasing
    order). At a given time slot, close the slot and check if a feasible schedule exists in the open slots. If so,
    leave the slot closed, otherwise, open it again. Continue to the next slot.
    :return:
    """
    time_horizon = instance.time_horizon
    jobs = instance.jobs

    for timeslot in time_horizon.time_slots:
        timeslot.is_open = False

        network = generate_network(time_horizon.time_slots, jobs)
        total_sum = sum(job.processing_time for job in jobs)
        schedule = solve_max_flow(network, total_sum, instance)

        if schedule.is_feasible:
            return schedule
        else:
            timeslot.is_open = True

    return Schedule(False, [])


def test_network():
    #TODO: Add this as a test for the algorithms
    instance = CustomInstance(6, 12, 2)
    instance.add_job(0, 0, 2, 2)
    instance.add_job(1, 0, 4, 2)
    instance.add_job(2, 1, 6, 1)
    instance.add_job(3, 0, 4, 4)

    network = generate_network(instance.time_horizon.time_slots, instance.jobs)
    network.print_network_info()
    total_sum = sum(job.processing_time for job in instance.jobs)

    answer = solve_max_flow(network, total_sum, instance)
    print(answer.is_feasible)
    print(answer.print_schedule_info()) # Total time Should be 5
