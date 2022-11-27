from input_generation.problem_instance import ProblemInstance


class AnalysisInputGenerator:

    @staticmethod
    def generate_multiple_instances(n: int, instance_type: str, g: int = -1):
        instances: list[ProblemInstance] = []
        for i in range(0, n):
            if instance_type == "Small":
                instances.append(ProblemInstance("Small set", g))
            elif instance_type == "Moderate":
                instances.append(ProblemInstance("Moderate set", g))
            else:
                instances.append(ProblemInstance("Large set", g))
        return instances

    @staticmethod
    def generate_multiple_feasible_instances(n: int, instance_type: str, g: int = -1):
        instances: list[ProblemInstance] = []
        for i in range(0, n):
            if instance_type == "Small":
                instance = AnalysisInputGenerator.generate_feasible_instance("Small set", g)
                instances.append(instance)
            elif instance_type == "Moderate":
                instance = AnalysisInputGenerator.generate_feasible_instance("Moderate set", g)
                instances.append(instance)
            else:
                instance = AnalysisInputGenerator.generate_feasible_instance("Large set", g)
                instances.append(instance)
        return instances

    @staticmethod
    def generate_feasible_instance(instance_type, g):
        instance = ProblemInstance(instance_type, g)
        while not instance.is_feasible():
            instance = ProblemInstance(instance_type, g)
        return instance

    @staticmethod
    def generate_infeasible_instance(instance_type, g):
        instance = ProblemInstance(instance_type, g)
        while instance.is_feasible():
            instance = ProblemInstance(instance_type, g)
        return instance
