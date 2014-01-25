#! /usr/bin/python3

"""
Simple script which generates the phrase 'ME THINKS ITS LIKE A WEASEL' using an extremely simple
genetic algorithm. This was completely inspired and based off what Richard Dawkin's performs in
his book 'The Blind Watchmaker' as a way of explaining accumulations of small change through the use
of cumulative selection.
"""

import random
from string import ascii_uppercase


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


def crossover(parent1, parent2):
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
    individual[index] = random.choice(ascii_uppercase + ' ')

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
    max_value = -10000
    for index, value in enumerate(numbers):
        if value > max_value:
            max_value = value
            max_index = index

    return max_index, max_value


if __name__ == '__main__':

    import time

    target = 'ME THINKS IT IS LIKE A WEASEL'
    population_size = 180  # Larger population sizes seem to be better
    mutation_rate = 0.20

    population = []
    for i in range(population_size):
        message = [random.choice(ascii_uppercase) for _ in range(len(target))]

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

    print 'Reached target in {}'.format(time.time() - t0)