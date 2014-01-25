Me thinks it is like a weasel!
==============================

Simple script which generates any given input phrase using an extremely simple
genetic algorithm.

This mini-task was completely inspired and based off what Richard Dawkin's performs in
his book 'The Blind Watchmaker' as a way of explaining accumulations of random small change to
generate complex sequences through selection and inheritance.

The script runs with Python 2.7

By default, the script will generate 'Me thinks it is like a Weasel' which is what Richard Dawkin's
uses for his example. The phrase is an excerpt from Hamlet. You can specify a different target as follows:

    python weasel.py --target "My Message Here"

Additionally, you can specify the mutation rate, the population size and which crossover operator to use:

    python weasel.py --mutation-rate 0.2  # Mutation rate of 20%

    python weasel.py --population-size 200  # Population size of 200

    python weasel.py --crossover 1X  # Use single point crossover
    python weasel.py --crossover uniform  # Use uniform crossover

You can view a detailed list of options by typing `python weasel.py -h' for the help.
