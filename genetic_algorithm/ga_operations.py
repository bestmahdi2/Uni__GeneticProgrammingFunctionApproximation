from genetic_algorithm.chromosome import *
from genetic_algorithm.population import Population


def traversal(position: int, chromosome: Chromosome) -> int:
    """
        Function to traverse the tree from the given position,

        Parameters:
            position (list): Start position
            chromosome (Chromosome): Chromosome to be traversed

        Returns:
            The value of traversal position
    """

    if chromosome.gen[position] in chromosome.terminal_set:
        return position + 1

    elif chromosome.gen[position] in chromosome.func_set[1]:
        return traversal(position + 1, chromosome)

    else:
        new_position = traversal(position + 1, chromosome)
        return traversal(new_position, chromosome)


def mutate(chromosome: Chromosome):
    """
        Function to mutate a chromosome,

        Parameters:
            chromosome (Chromosome): Chromosome to be mutated

        Returns:
            chromosome: The mutated chromosome
    """

    position = np.random.randint(len(chromosome.gen))

    if chromosome.gen[position] in chromosome.func_set[1] + chromosome.func_set[2]:
        if chromosome.gen[position] in chromosome.func_set[1]:
            chromosome.gen[position] = random.choice(chromosome.func_set[1])

        else:
            chromosome.gen[position] = random.choice(chromosome.func_set[2])

    else:
        chromosome.gen[position] = random.choice(chromosome.terminal_set)

    return chromosome


def selection(population: Population, num_sel: int) -> Chromosome:
    """
        Function to select a member of the population for crossing over,

        Parameters:
            population (Population): Population of chromosomes
            num_sel (int): Number of chromosome selected from the population

        Returns:
            best: The selected chromosome
    """

    sample = random.sample(population.list, num_sel)
    best = sample[0]

    for i in range(1, len(sample)):
        if population.list[i].fitness < best.fitness:
            best = population.list[i]

    return best


def cross_over(mother: Chromosome, father: Chromosome, max_depth: int) -> Chromosome:
    """
        Function to cross over two chromosomes in order to obtain a child,

        Parameters:
            mother (Chromosome): Chromosome
            father (Chromosome): Chromosome
            max_depth (int): Maximum_depth of a tree

        Returns:
            child: The child chromosome
    """

    child = Chromosome(mother.terminal_set, mother.func_set, mother.depth, None)

    start_m = np.random.randint(len(mother.gen))
    start_f = np.random.randint(len(father.gen))

    end_m = traversal(start_m, mother)
    end_f = traversal(start_f, father)

    child.gen = mother.gen[:start_m] + father.gen[start_f: end_f] + mother.gen[end_m:]

    if child.get_depth() > max_depth and random.random() > 0.2:
        child = Chromosome(mother.terminal_set, mother.func_set, mother.depth)

    return child


def get_best(population: Population) -> Chromosome:
    """
        Function to get the best chromosome from the population,

        Parameters:
            population (Population): Population to get the best chromosome from

        Returns:
            best: The best chromosome from population
    """

    best = population.list[0]

    for i in range(1, len(population.list)):
        if population.list[i].fitness < best.fitness:
            best = population.list[i]

    return best


def get_worst(population: Population) -> Chromosome:
    """
        Function to get the worst chromosome of the population,

        Parameters:
            population (Population): Population to get the best chromosome from

        Returns:
            worst: The worst chromosome from the population
    """

    worst = population.list[0]

    for i in range(1, len(population.list)):
        if population.list[i].fitness > worst.fitness:
            worst = population.list[i]

    return worst


def replace_worst(population: Population, chromosome: Chromosome) -> Population:
    """
        Function to change the worst chromosome of the population with a new one,

        Parameters:
            population (Population): Population to get the best chromosome from
            chromosome (Chromosome): Chromosome to be added

        Returns:
            population: The replaced population
    """

    worst = get_worst(population)

    if chromosome.fitness < worst.fitness:
        for i in range(len(population.list)):
            if population.list[i].fitness == worst.fitness:
                population.list[i] = chromosome
                break

    return population


def roulette_selection(population: Population) -> Population:
    """
        Function to select a member of the population using roulette selection,

        Parameters:
            population (Population): Population to be selected from

        Returns:
            The selection of population
    """

    fitness = [chrom.fitness for chrom in population.list]
    order = [x for x in range(len(fitness))]
    order = sorted(order, key=lambda x: fitness[x])
    fs = [fitness[order[i]] for i in range(len(fitness))]

    sum_fs = sum(fs)
    max_fs = max(fs)
    min_fs = min(fs)

    p = random.random() * sum_fs
    t = max_fs + min_fs

    chosen = order[0]

    for i in range(len(fitness)):
        p -= (t - fitness[order[i]])
        if p < 0:
            chosen = order[i]
            break

    return population.list[chosen]
