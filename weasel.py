#! /usr/bin/python3

"""
Simple script which generates the phrase 'ME THINKS ITS LIKE A WEASEL' using an extremely simple
genetic algorithm. This was completely inspired and based off what Richard Dawkin's performs in
his book 'The Blind Watchmaker' as a way of explaining accumulations of small change through the use
of cumulative selection.
"""

import random
from string import ascii_uppercase


def mutation(individual, rate=0.01):
    for index, _ in enumerate(individual):
        if random.random() < rate:
            individual[index] = random.choice(ascii_uppercase)

    return individual


def fitness(message, target):
    value = 0
    for i in range(target):
        value += 1 if message[i] == target[i] else 0

    return value


def evaluate(population):
    fitness_values = []
    for individual in population:
        fitness_values.append(fitness(individual))

    return fitness_values


# Roulette wheel selection
def selection(fitness_values):

    choice = random.randint(sum(fitness_values))
    for index, value in enumerate(fitness_values):
        choice -= value

        if choice < 0:
            return index


if __name__ == '__main__':

    target = 'ME THINKS ITS LIKE A WEASEL'
    population_size = 10

    population = []
    for i in range(population_size):
        message = ''.join([random.choice(ascii_uppercase) for _ in range(len(target))])

        population.append(message)

    while True:
        fitness_values = evaluate(population)
