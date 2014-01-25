"""
Simple script which generates the phrase 'ME THINKS ITS LIKE A WEASEL' using an extremely simple
genetic algorithm. This was completely inspired and based off what Richard Dawkin's performs in
his book 'The Blind Watchmaker' as a way of explaining accumulations of small change through the use
of cumulative selection.
"""

import sys
import random
from string import ascii_letters, digits
from copy import copy

alphabet = ascii_letters + ' ' + digits


def tournament(population, target, n):

    result = []

    while len(result) < n:
        c1 = random.choice(population)
        c2 = random.choice(population)

        if fitness(c1, target) > fitness(c2, target):
            result.append(c1)
            population.remove(c1)
        else:
            result.append(c2)
            population.remove(c2)

    return result


def single_point_crossover(parent1, parent2):
    child1 = copy(parent1)
    child2 = copy(parent2)

    split_point = random.randint(1, len(parent1) - 2)

    for index in xrange(len(parent1)):
        if index < split_point:
            child1[index] = parent2[index]
        else:
            child2[index] = parent1[index]

    return child1, child2

def uniform_crossover(parent1, parent2):
    # Uniform crossover
    child1 = []
    child2 = []

    for index, _ in enumerate(parent1):
        if random.random() < 0.5:
            child1.append(parent1[index])
            child2.append(parent2[index])
        else:
            child1.append(parent2[index])
            child2.append(parent1[index])

    return child1, child2


def mutation(individual):
    index = random.randint(0, len(individual) - 1)
    individual[index] = random.choice(alphabet)

    return individual


def fitness(message, target):
    value = 0
    for index, actual in enumerate(target):
        value += 1 if message[index] == actual else 0

    return value


def evaluate(population, target):
    fitness_values = []
    for individual in population:
        fitness_values.append(fitness(individual, target))

    return fitness_values


# Roulette wheel selection
def selection(population, fitness_values):

    results = []
    while len(results) < 2:
        choice = random.randint(0, sum(fitness_values))
        for index, value in enumerate(fitness_values):
            choice -= value

            if choice < 0:
                results.append(population[index])

    return results[0], results[1]


def argmax(numbers):

    max_index = None
    max_value = -sys.maxint - 1
    for index, value in enumerate(numbers):
        if value > max_value:
            max_value = value
            max_index = index

    return max_index, max_value


if __name__ == '__main__':

    import time
    import argparse

    parser = argparse.ArgumentParser(description='Evolve an input sentence using a genetic algorithm')
    parser.add_argument('--target', type=str, default='Me thinks it is like a Weasel')
    parser.add_argument('--mutation-rate', '-m', type=float, default=0.20)
    parser.add_argument('--population-size', '-p', type=int, default=180)
    parser.add_argument('--crossover', '-c', choices=('1X', 'uniform'), type=str, default='uniform')

    args = parser.parse_args()

    crossover_operators = {
        '1X': single_point_crossover,
        'uniform': uniform_crossover,
    }

    # Extract the parameters from the arguments
    target = args.target
    population_size = args.population_size
    mutation_rate = args.mutation_rate
    crossover = crossover_operators[args.crossover]

    population = []
    for i in range(population_size):
        message = [random.choice(alphabet) for _ in range(len(target))]

        population.append(message)

    t0 = time.time()
    count = 0

    print 'Target = {}'.format(target)
    while True:
        fitness_values = evaluate(population, target)
        count += 1

        max_index, max_value = argmax(fitness_values)

        best = ''.join(population[max_index])
        print 'Gen {}: {} ({})'.format(count, best, max_value)

        if best == target:
            break

        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = selection(population, fitness_values)

            child1, child2 = crossover(parent1, parent2)

            if random.random() < mutation_rate:
                mutation(child1)
            if random.random() < mutation_rate:
                mutation(child2)

            new_population.append(child1)
            new_population.append(child2)

        population = tournament(population + new_population, target, population_size)

    print 'Reached target in {0:.3g} seconds'.format(time.time() - t0)
