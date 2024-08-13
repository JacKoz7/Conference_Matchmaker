def print_outcome(algorithm, solution) -> None:
    for i in range(len(algorithm.give_desired_attributes(solution))):
        print(
            f"Participant {i+1} desired attributes: {algorithm.give_desired_attributes(solution)[i]}"
        )
    print()

    for j in range(len(algorithm.give_attributes(solution))):
        print(
            f"Attributes of participants matched for Participant {j+1}: {algorithm.give_attributes(solution)[j]}"
        )
    print()

    for k in range(len(algorithm.find_matches(solution))):
        print(f"Participant {k+1} matches: {algorithm.find_matches(solution)[k]}")
    print()

    for i, p in enumerate(solution.values()):
        participants_ids = ", ".join(map(str, p))
        print(
            f"Participant number {i + 1} matched with participants with IDs {participants_ids}"
        )
