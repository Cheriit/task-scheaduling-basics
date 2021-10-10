import sys
from typing import List

from algorithms import Algorithm, SingleRSLmaxAlgorithm

instance_sizes: List[int] = list(range(50, 251, 50))
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
    if algorithm == '1-rs-Lmax':
        return SingleRSLmaxAlgorithm()
    else:
        raise ValueError('Unknown algorithm')


def use_action(action: str, algorithm: Algorithm):
    if action == 'generate':
        for n in instance_sizes:
            algorithm.generate(prefix_value, n)
    elif action == 'validate':
        algorithm.validate()
    else:
        raise ValueError('Unknown action')


if __name__ == '__main__':
    main()
