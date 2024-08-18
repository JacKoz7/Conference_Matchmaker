import sys

from dataloader import load_from_file
from matching import Algorithm
from resultprinter import print_solution


def run(input_file: str, iterations: int = 100000):
    participants = load_from_file(input_file)

    alg = Algorithm(participants)

    final_solution = alg.run(iterations)

    print_solution(participants, final_solution)


if __name__ == "__main__":
    file = sys.argv[1]
    run(file)
