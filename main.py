import click

from src.dataloader import Dataloader
from src.matching import Algorithm
from src.resultprinter import print_solution


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--iterations", "-i", default=100_000, help="Number of iterations", type=int
)
@click.option(
    "--recommendations",
    "-r",
    default=5,
    help="How many recommendations each participant should receive",
    type=int,
)
@click.option(
    "--noimprovement",
    "-ni",
    default=1000,
    help="Number of consecutive iterations without score improvement before the algorithm stops",
    type=int,
)
def run(
    input_file: str, iterations: int, recommendations: int, noimprovement: int
) -> None:
    data = Dataloader(input_file)

    if iterations < 1000:
        raise click.BadParameter(f"Iterations must be at least 1000. Got {iterations}.")

    all_particpants = data.count_participants()
    if recommendations < 1 or recommendations > all_particpants - 1:
        raise click.BadParameter(
            f"Recommendations must be between 1 and the maxium number of participants minus 1 ({all_particpants - 1}). Got {recommendations}."
        )
    if noimprovement < 1 or noimprovement > iterations:
        raise click.BadParameter(
            f"No improvement iterations must be between 0 and the total number of iterations. "
            f"Got {noimprovement}, while total iterations are {iterations}."
        )

    participants = data.load_from_file()

    alg = Algorithm(participants, recommendations)

    final_solution = alg.run(iterations, noimprovement)

    print_solution(final_solution)


if __name__ == "__main__":
    run()
