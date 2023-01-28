from problem_classes.problem_instances import ProblemInstance


class DatasetGenerator:
    """
    DatasetGenerator class containing static methods for generating datasets with problem instances.
    """

    @staticmethod
    def generate_multiple_instances(n: int, instance_type: str, number_of_jobs: int,
                                    number_of_timeslots: int, batch_size: int):
        """
        Generate a list containing <n> problem instances of <instance_type> with <g> as a parameter
        """

        instances: list[ProblemInstance] = []
        for i in range(0, n):
            if instance_type == "Small":
                instances.append(ProblemInstance("Small", number_of_jobs, number_of_timeslots, batch_size))
            elif instance_type == "Moderate":
                instances.append(ProblemInstance("Moderate", number_of_jobs, number_of_timeslots, batch_size))
            else:
                instances.append(ProblemInstance("Large", number_of_jobs, number_of_timeslots, batch_size))
        return instances

    @staticmethod
    def generate_multiple_feasible_instances(n: int, instance_type: str, number_of_jobs:
    int, number_of_timeslots: int, batch_size: int):
        """
        Generate a list containing <n> feasible problem instances of <instance_type> with <g> as a parameter
        """

        instances: list[ProblemInstance] = []
        for i in range(0, n):
            instance = DatasetGenerator.generate_feasible_instance(instance_type, number_of_jobs,
                                                                   number_of_timeslots, batch_size)
            instances.append(instance)
        return instances

    @staticmethod
    def generate_feasible_instance(instance_type: str, number_of_jobs:
    int, number_of_timeslots: int, batch_size: int):
        """
        Generate a feasible problem instance of <instance_type> with <g> as a parameter
        """

        instance = ProblemInstance(instance_type, number_of_jobs, number_of_timeslots, batch_size)
        while not instance.is_feasible():
            instance = ProblemInstance(instance_type, number_of_jobs, number_of_timeslots, batch_size)
        return instance

    @staticmethod
    def generate_infeasible_instance(instance_type: str, number_of_jobs:
    int, number_of_timeslots: int, batch_size: int):
        """
        Generate an infeasible problem instance of <instance_type> with <g> as a parameter
        """

        instance = ProblemInstance(instance_type, number_of_jobs, number_of_timeslots, batch_size)
        while instance.is_feasible():
            instance = ProblemInstance(instance_type, number_of_jobs, number_of_timeslots, batch_size)
        return instance
