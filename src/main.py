import sys

from dataloader import load_from_file
from matching import Algorithm
from resultprinter import print_solution


def run(file: str, iterations: int = 100):
    participants = load_from_file(file)

    alg = Algorithm(participants)

    final_solution = alg.run(iterations)

    print_solution(alg, final_solution)


if __name__ == "__main__":
    file = sys.argv[1]
    run(file)
