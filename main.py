import click

from src.dataloader import load_from_file
from src.matching import Algorithm
from src.resultprinter import print_solution


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--iterations", "-i", default=100_000, help="Number of iterations", type=int
)
@click.option(
    "--recommendations",
    default=5,
    help="Number of recommendations",
    type=int,
)
@click.option("--noimprovement", default=10_000,
              help="Number of consecutive iterations without score improvement before the algorithm stops", type=int)
def run(input_file: str, iterations: int, recommendations: int, noimprovement: int) -> None:
    if iterations < 1000:
        raise click.BadParameter(f"Iterations must be at least 1000. Got {iterations}.")

    if recommendations < 1 or recommendations > 10:
        raise click.BadParameter(
            f"Recommendations must be between 1 and 10. " f"Got {recommendations}."
        )
    if noimprovement < 1 or noimprovement > iterations:
        raise click.BadParameter(
            f"No improvement iterations must be between 0 and the total number of iterations. "
            f"Got {noimprovement}, while total iterations are {iterations}."
        )


    participants = load_from_file(input_file)

    alg = Algorithm(participants, recommendations)

    final_solution = alg.run(iterations, noimprovement)

    print_solution(final_solution)


if __name__ == "__main__":
    run()
