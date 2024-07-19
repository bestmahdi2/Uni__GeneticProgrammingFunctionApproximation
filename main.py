import time
import math
import matplotlib.pyplot as plt
from genetic_algorithm.algorithm import *
from genetic_algorithm.population import *


class Main:
    """
        Class for main
    """

    def __init__(self, use_method=True) -> None:
        """
            Constructor for Main class,
        """

        start_time = time.time()

        # it's 1D function
        terminal_set = ['x0']

        # tree
        max_depth = 20
        default_depth = 6

        # population
        population_num = 8000
        selected_chromosomes = 20
        epoch_feedback = 100

        # default functions and operators
        functions = {1: ['sin', 'cos'],
                     2: ['+', '*', '^', '-', '/']}

        # additional functions
        functions[1] += ['abs', 'sqrt', 'tg', 'ctg', 'e', 'ln', 'tanh', ]

        if use_method:
            # x range
            x_start_range = -10
            x_end_range = +10
            x_steps = 0.03

            # create x and y
            X = self.create_all_points_x(x_start_range, x_end_range, x_steps)
            Y = self.create_all_points_y(X)

        else:
            # read x and y from file
            X, Y = self.read_all_points()

        # create population
        population = Population(population_num, selected_chromosomes, functions, terminal_set, default_depth, max_depth)

        # do the algorithm on population
        algorithm = Algorithm(population, population_num, X, Y, epoch_feedback)

        # train the algorithm
        best_function, found_functions = algorithm.train()

        # predict y in best function
        y_pred = [[best_function.evaluate_arg(x)] for x in X]

        # show results of function and fitness in terminal
        self.show_results(start_time, best_function, found_functions)

        # make a plot and show two functions
        self.plot_show(X, Y, y_pred)

    def f(self, x: float) -> float:
        """
            F function,

            Parameters:
                x (float): The input x

            Returns:
                The result of the function F
        """

        # return self.case1_f(x)
        # return self.case2_f(x)
        # return self.case3_f(x)
        # return self.case4_1_f(x)
        # return self.case4_2_f(x)
        # return self.case4_3_f(x)
        return self.case4_4_f(x)

    @staticmethod
    def case1_f(x):
        # return math.tan(x) + x
        return x ** 2 + 2 * x / 5

    @staticmethod
    def case2_f(x):
        # strange function
        if int(round(x)) % 2 == 0:
            return x + 5 * math.cos(x) ** 3

        else:
            return 10 * math.sin(x / 2)

    @staticmethod
    def case3_f(x):
        if x < -5:
            return x ** 2

        elif -5 <= x <= 5:
            return -x - 3

        else:
            return x ** 2

    @staticmethod
    def case4_1_f(x):
        return x * 4

    @staticmethod
    def case4_2_f(x):
        return x ** 3

    @staticmethod
    def case4_3_f(x):
        return 2 ** x

    @staticmethod
    def case4_4_f(x):
        return math.tanh(x) + 1

    @staticmethod
    def create_all_points_x(x_start_range: int, x_end_range: int, x_steps: float) -> list:
        """
            Method to create x of points,

            Parameters:
                x_start_range (int): Start range of x
                x_end_range (int): End of range of x
                x_steps (float): Steps of forwarding from start of x to the end

            Returns:
                The list of points
        """

        return [[x] for x in np.arange(x_start_range, x_end_range, x_steps)]

    def create_all_points_y(self, x_list: list) -> list:
        """
            Method to create y of points,

            Parameters:
                x_list (list): The list of points to find y

            Returns:
                y_list: The list of points
        """

        y_list = [[self.f(x[0])] for x in x_list]

        # make tuple of points x, y
        keeper = [f"({x[0]}, {y_list[x_list.index(x[0])][0]})" for x in x_list]

        # save to file
        with open("points.txt", "w") as file:
            file.write("\n".join(keeper))

        return y_list

    @staticmethod
    def read_all_points() -> Tuple[list, list]:
        """
            Method to read points from file,

            Returns:
                The list of points
        """

        # read the file
        with open("points.txt", "r") as file:
            lines = [i.replace(")", "").replace("(", "").split(", ") for i in file.readlines()]

        X, Y = [], []
        for line in lines:
            X.append([round(float(line[0]), 5)])
            Y.append([round(float(line[1]), 5)])

        return X, Y

    @staticmethod
    def show_results(start_time: float, best_function: Chromosome, found_functions: list) -> None:
        """
            Method to show the fitness and found functions,

            Parameters:
                best_function (Chromosome): The chromosome of best function matching
                found_functions (list): The list of all found functions
        """

        print("\n----------------------\n")

        if len(found_functions):
            print("< Tested Bests >\n")

            x = 0
            while x < len(found_functions):
                print(f"{x + 1}) f(): {found_functions[x][0]} -- Fitness: {found_functions[x][1]}")
                x += 1

        print("\n----------------------\n")

        print("< Best Tree Function >\n\n", best_function.gen)

        print("\n----------------------\n")

        print(f"< Running Time >")
        print(f"> {(time.time() - start_time)} seconds !")

    @staticmethod
    def plot_show(x_list: list, y_list: list, predicted_y_list: list) -> None:
        """
            Method to show the created plot using last function and predicted function,

            Parameters:
                x_list (list): The list of all points (x)
                y_list (list): The list of all points (y)
                predicted_y_list (list): The list of all predicted points (y`)
        """

        # create the function with function
        plt.plot(x_list, y_list,
                 color='b', linestyle='dashed', label='Expected')

        # create the function with predicted function
        plt.plot(x_list, predicted_y_list,
                 color='r', linestyle='dashed', label='Predicted')

        plt.show()  # show the plot


if __name__ == '__main__':
    # To use f method to create points,
    # otherwise it read the points from file
    use_method = True

    M = Main(use_method)
