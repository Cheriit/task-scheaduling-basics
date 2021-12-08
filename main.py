import sys
from typing import List
from os import listdir
from os.path import isfile, join

from algorithms import Algorithm, SingleRSLmaxAlgorithm, Q4RSumWUAlgorithm, F4EwDwAlgorithm

instance_sizes: List[int] = list(range(50, 501, 50))
prefix_value: str = '141320'


def main():
    """
    Algorithms runner.
    Runner requires 2 system parameters:
    - algorithm (1-rs-Lmax)
    - action (generate, validate)
    """
    args = sys.argv
    if len(args) >= 3:
        algorithm = select_algorithm(args[1])
        use_action(args[2], algorithm)
    else:
        raise ValueError('Not enough parameters to run program')


def select_algorithm(algorithm: str) -> Algorithm:
    if algorithm == '1-RS-Lmax':
        return SingleRSLmaxAlgorithm()
    if algorithm == 'Q4-R-SumWU':
        return Q4RSumWUAlgorithm()
    if algorithm == 'F4--EwDw':
        return F4EwDwAlgorithm()
    else:
        raise ValueError('Unknown algorithm')


def use_action(action: str, algorithm: Algorithm):
    if action == 'generate':
        for n in instance_sizes:
            algorithm.generate(prefix_value, n)
    if action == 'validate' or action == 'generate':
        args = sys.argv
        if len(args) >= 4:
            algorithm.validate(args[3])
        else:
            files = [f for f in listdir('./out') if isfile(join('./out', f))]
            for file in files:
                if file != '.gitkeep':
                    algorithm.validate(file)
    elif action == 'solve':
        files = [f for f in listdir('./in') if isfile(join('./in', f))]
        score = 0
        for file in files:
            if file != '.gitkeep':
                score += algorithm.schedule_tasks(file)
        print(score)

    elif action == 'mock':
        files = [f for f in listdir('./in') if isfile(join('./in', f))]
        for file in files:
            if file != '.gitkeep':
                algorithm.create_mock_result_file(file)
    else:
        raise ValueError('Unknown action')


if __name__ == '__main__':
    main()
