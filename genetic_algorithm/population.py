from typing import List
from genetic_algorithm.chromosome import *
from genetic_algorithm.chromosome import Chromosome


class Population:
    """
        This is a class for representing a population of chromosomes.

        Attributes:
            size (int): Number of members in the population
            num_selected (int): Number of chromosomes selected from the population
            func_set (dict): Set of functions for the population
            terminal_set (list): Set of terminals for the population
            depth (int): Initial depth of a tree
            max_depth (int): Maximum depth of a tree
    """

    def __init__(self, size: int, num_selected: int, func_set: dict, terminal_set: list, depth: int,
                 max_depth: int) -> None:
        """
            Constructor for population class,

            Parameters:
                size (int): Number of members in the population
                num_selected (int): Number of chromosomes selected from the population
                func_set (dict): Set of functions for the population
                terminal_set (list): Set of terminals for the population
                depth (int): Initial depth of a tree
                max_depth (int): Maximum depth of a tree
        """

        self.size = size
        self.max_depth = max_depth
        self.num_selected = num_selected
        self.list = self.create_population(self.size, func_set, terminal_set, depth)

    def create_population(self, number: int, func_set: dict, terminal_set: list, depth: int) -> List[Chromosome]:
        """
            Method to create population,

            Parameters:
                number (int): Number of members in the population
                func_set (dict): Set of functions for the population
                terminal_set (list): Set of terminals for the population
                depth (int): Initial depth of a tree

            Returns:
                pop_list: List of population

        """

        pop_list = []

        for i in range(number):
            if random.random() > 0.5:
                pop_list.append(Chromosome(terminal_set, func_set, depth, 'grow'))

            else:
                pop_list.append(Chromosome(terminal_set, func_set, depth, 'full'))

        return pop_list
