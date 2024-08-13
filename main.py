from dataloader import load_from_file
from matchingalgorithm import Algorithm
from displayoutcome import print_outcome

if __name__ == "__main__":
    participants = load_from_file("inputdata.txt")

    mainalgorithm = Algorithm(participants)

    sol = mainalgorithm.random_solution()

    mainalgorithm.mutate(sol)

    best_matches = mainalgorithm.run(10000)

    print_outcome(mainalgorithm, best_matches)






