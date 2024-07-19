import random
import warnings
import numpy as np
from typing import Tuple, Any, Union

warnings.filterwarnings("error")


class Chromosome:
    """
       This is a class for representing a chromosome.

       Attributes:
            terminal_set (list): Set of terminals
            funct_set (dict): Set of functions
            depth (int): Tree depth
            method (str): Method to generate the tree, default is full
    """

    def __init__(self, terminal_set: list, funct_set: dict, depth: int, method: Union[str, None] = 'full') -> None:
        """
            Constructor for Chromosome class,

            Parameters:
                terminal_set (list): Set of terminals
                funct_set (dict): Set of functions
                depth (int): Tree depth
                method (str): Method to generate the tree, default is full
        """

        self.depth = depth
        self.terminal_set = terminal_set
        self.func_set = funct_set
        self.gen = []
        self.fitness = None

        if method == 'grow':
            self.grow()

        elif method == 'full':
            self.full()

    def full(self, level: int = 0) -> None:
        """
            Method to generate a tree in a full manner,
            * Every node will have exactly two children.
        """

        if level == self.depth:
            self.gen.append(random.choice(self.terminal_set))

        else:
            val = random.choice(self.func_set[1] + self.func_set[2])

            if val in self.func_set[2]:
                self.gen.append(random.choice(self.func_set[2]))
                self.full(level + 1)
                self.full(level + 1)

            else:
                self.gen.append(random.choice(self.func_set[1]))
                self.full(level + 1)

    def grow(self, level: int = 0) -> None:
        """
            Method to generate a tree in a growth manner,
            Every node may be a terminal or a function.
        """

        if level == self.depth:
            self.gen.append(random.choice(self.terminal_set))

        else:
            if random.random() > 0.3:
                val = random.choice(self.func_set[2] + self.func_set[1])

                if val in self.func_set[2]:
                    self.gen.append(val)
                    self.grow(level + 1)
                    self.grow(level + 1)

                else:
                    self.gen.append(val)
                    self.grow(level + 1)

            else:
                val = random.choice(self.terminal_set)
                self.gen.append(val)

    def eval(self, input_functions: list, position: int = 0) -> Tuple[Any, int]:
        """
            Method to evaluate the current chromosome with a given input,

            Parameters:
                input_functions (list): Method input (x0, x1... xn)
                position (int): current position in genotype 
        """

        if self.gen[position] in self.terminal_set:
            return input_functions[int(self.gen[position][1:])], position

        elif self.gen[position] in self.func_set[2]:
            position_op = position
            left, position = self.eval(input_functions, position + 1)
            right, position = self.eval(input_functions, position + 1)

            if self.gen[position_op] == '+':
                return left + right, position

            elif self.gen[position_op] == '-':
                return left - right, position

            elif self.gen[position_op] == '*':
                return left * right, position

            elif self.gen[position_op] == '^':
                return left ** right, position

            elif self.gen[position_op] == '/':
                return left / right, position

        else:
            position_op = position
            left, position = self.eval(input_functions, position + 1)

            if self.gen[position_op] == 'sin':
                return np.sin(left), position

            elif self.gen[position_op] == 'cos':
                return np.cos(left), position

            elif self.gen[position_op] == 'ln':
                return np.log(left), position

            elif self.gen[position_op] == 'sqrt':
                return np.sqrt(left), position

            elif self.gen[position_op] == 'tg':
                return np.tan(left), position

            elif self.gen[position_op] == 'ctg':
                return 1 / np.tan(left), position

            elif self.gen[position_op] == 'e':
                return np.exp(left), position

            elif self.gen[position_op] == 'tanh':
                return np.tanh(left), position

            elif self.gen[position_op] == 'abs':
                return abs(left), position

    def evaluate_arg(self, input_x: list):
        """
            Method to evaluate the current genotype to a given input,

            Parameters:
                input_x (list): Inputs of the function we want to predict

            Returns:
                The value of self.gen evaluated at the given input
        """

        return self.eval(input_x)[0]

    def calculate_fitness(self, inputs: list, outputs: list):
        """
            Method to calculate the fitness of a chromosome,

            Parameters:
                inputs (list): Inputs of the function we want to predict
                outputs (list): Outputs of the function we want to predict

            Returns:
                self.fitness: The chromosome's fitness (calculated based on MSE)
        """

        diff = 0

        for i in range(len(inputs)):
            try:
                diff += (self.eval(inputs[i])[0] - outputs[i][0]) ** 2

            except RuntimeWarning:
                self.gen = []

                if random.random() > 0.5:
                    self.grow()

                else:
                    self.full()

                self.calculate_fitness(inputs, outputs)

        if len(inputs) == 0:
            return 1e9

        self.fitness = diff / (len(inputs))
        return self.fitness

    def __get_depth_aux(self, position: int = 0) -> Tuple[int, int]:
        """
            Method to get the depth of a chromosome,

            Parameters:
                position (list): Inputs of the function we want to predict

            Returns:
                Chromosome's depth, last pos
        """

        elem = self.gen[position]

        if elem in self.func_set[2]:
            left, position = self.__get_depth_aux(position + 1)
            right, position = self.__get_depth_aux(position)

            return 1 + max(left, right), position

        elif elem in self.func_set[1]:
            left, position = self.__get_depth_aux(position + 1)
            return left + 1, position

        else:
            return 1, position + 1

    def get_depth(self):
        """
            Method to get the depth of a chromosome,

            Returns:
                Chromosome's depth
        """

        return self.__get_depth_aux()[0] - 1
