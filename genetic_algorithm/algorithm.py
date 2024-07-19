from tqdm import tqdm
from typing import List
from genetic_algorithm.ga_operations import *
from genetic_algorithm.population import Population


class Algorithm:
    """
        This is a class for representing the algorithm.

        Attributes:
            population (Population): Population for the current algorithm
            iterations (int): Number of iterations for the algorithm
            inputs (list): Inputs (x list)
            outputs (list): Outputs (x list)
            epoch_feedback (int): Number of epochs to show feedback
    """

    def __init__(self, population: Population, iterations: int, inputs: list, outputs: list, epoch_feedback: int = 100):
        """
            Constructor for Algorithm class,

            Parameters:
                population (Population): Population for the current algorithm
                iterations (int): Number of iterations for the algorithm
                inputs (list): Inputs (x list)
                outputs (list): Outputs (x list)
                epoch_feedback (int): Number of epochs to show feedback
        """

        self.population = population
        self.iterations = iterations
        self.inputs = inputs
        self.outputs = outputs
        self.epoch_feedback = epoch_feedback

    def __one_step(self) -> None:
        """
            Method to do one step of the algorithm,
        """

        # get a selection of random members of population
        mother = selection(self.population, self.population.num_selected)

        # get a different selection of random members of population
        father = selection(self.population, self.population.num_selected)

        # cross over two chromosomes to obtain a child
        child = cross_over(mother, father, self.population.max_depth)
        child = mutate(child)

        child.calculate_fitness(self.inputs, self.outputs)

        # replace the worst chromosome with a new one
        self.population = replace_worst(self.population, child)

    def train(self) -> List[Union[Chromosome, List[Union[List[Any], Any]]]]:
        """
            Method to train the algorithm,
        """

        best_keeper = []

        # progress bar for population
        pbar1 = tqdm(total=len(self.population.list), desc="Population")

        # calculate fitness of population
        for i in range(len(self.population.list)):
            self.population.list[i].calculate_fitness(self.inputs, self.outputs)
            pbar1.update(n=1)

        progress_list = [i for i in range(self.iterations) if not (i % self.epoch_feedback)]

        max_progress = len(progress_list)

        # for i in range(self.iterations):
        #     if i % self.epoch_feedback == 0:
        #         max_progress += 1

        print()

        # progress bar for best
        pbar2 = tqdm(total=max_progress, desc="Best")

        # find the bests
        for i in range(self.iterations):
            if i % self.epoch_feedback == 0:
                best_so_far = get_best(self.population)
                best_keeper.append([best_so_far.gen, best_so_far.fitness])
                pbar2.update(n=1)

            self.__one_step()

        return [get_best(self.population),
                [best_keeper[i] for i in range(len(best_keeper)) if i == best_keeper.index(best_keeper[i])]]
