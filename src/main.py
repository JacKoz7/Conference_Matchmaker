import sys

from dataloader import load_from_file
from matchingalgorithm import Algorithm
from displayoutcome import print_outcome


def run(file):
    participants = load_from_file(file)

    mainalgorithm = Algorithm(participants)

    sol = mainalgorithm.random_solution()

    mainalgorithm.mutate(sol)

    best_matches = mainalgorithm.run(100)

    print_outcome(mainalgorithm, best_matches)


if __name__ == "__main__":
    input_file = sys.argv[1]
    run(input_file)
