import sys
import click

from src.dataloader import load_from_file
from src.matching import Algorithm
from src.resultprinter import print_solution


def run(input_file: str, iterations: int = 100000) -> None:
    participants = load_from_file(input_file)

    alg = Algorithm(participants)

    final_solution = alg.run(iterations)

    print_solution(final_solution)


if __name__ == "__main__":
    file: str = sys.argv[1]
    run(file)
