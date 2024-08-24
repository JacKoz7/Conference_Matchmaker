import click

from src.dataloader import load_from_file
from src.matching import Algorithm
from src.resultprinter import print_solution


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--iterations", "-i", default=100000, help="Number of iterations", type=int
)
@click.option(
    "--recommendations",
    "--recom",
    default=5,
    help="Number of recommendations",
    type=int,
)
def run(input_file: str, iterations: int, recommendations: int) -> None:
    if iterations < 1000:
        raise click.BadParameter(f"Iterations must be at least 1000. Got {iterations}.")

    if recommendations < 1 or recommendations > 10:
        raise click.BadParameter(
            f"Recommendations must be between 1 and 10. " f"Got {recommendations}."
        )

    participants = load_from_file(input_file)

    alg = Algorithm(participants, recommendations)

    final_solution = alg.run(iterations)

    print_solution(final_solution)


if __name__ == "__main__":
    run()
