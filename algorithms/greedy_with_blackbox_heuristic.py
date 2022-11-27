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
    if instance.is_feasible: # Check feasibility
        for timeslot in time_horizon.time_slots:
            timeslot.is_open = False

            network = generate_network(time_horizon.time_slots, jobs)
            total_sum = sum(job.processing_time for job in jobs)
            schedule = solve_max_flow(network, total_sum, instance)

            if schedule.is_feasible:
                return schedule
            else:
                timeslot.is_open = True

    return Schedule(instance.jobs, instance.time_horizon.time_slots, False)


def test_network():
    time_horizon: TimeHorizon = TimeHorizon(6, 2)
    jobs: list[Job] = []
    job1 = Job(1)
    job1.release_time = 0
    job1.deadline = 2
    job1.processing_time = 2
    jobs.append(job1)

    job2 = Job(2)
    job2.release_time = 0
    job2.deadline = 4
    job2.processing_time = 2
    jobs.append(job2)

    job3 = Job(3)
    job3.release_time = 1
    job3.deadline = 6
    job3.processing_time = 1
    jobs.append(job3)

    job4 = Job(4)
    job4.release_time = 0
    job4.deadline = 4
    job4.processing_time = 4
    jobs.append(job4)

    # times = time_horizon.time_slots
    # # for time in times:
    # #     time.is_open = False
    #
    # network = generate_network(times, jobs)
    # # network2 = generate_network(times, jobs)
    # # print(network.get_arcs_as_tuples() == network2.get_arcs_as_tuples())
    # # # network.print_network_info()
    # total_sum = sum(job.processing_time for job in jobs)
    # time = solve_max_flow(network, total_sum)
    # print(time)

    answer = greedy_with_blackbox_heuristic(time_horizon, jobs)
    print(answer)
