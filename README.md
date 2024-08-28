# Conference Matchmaker
An innovative solution for optimizing networking at business conferences!

## About
The system analyzes the attributes and preferences of conference participants to suggest the most suitable people for each attendee to connect with. The goal is to maximize the value of interactions between participants by matching them based on their possessed and sought-after characteristics.

## Evaluation
```bash
# install dependencies
$ pip install -r requirements.txt

# display usage
$ python3 main.py --help
Usage: main.py [OPTIONS] INPUT_FILE

Options:
  -i, --iterations INTEGER       Number of iterations
  -r, --recommendations INTEGER  How many recommendations each participant
                                 should receive
  -ni, --noimprovement INTEGER   Number of consecutive iterations without
                                 score improvement before the algorithm stops
  --help                         Show this message and exit.

# example usage
$ python3 main.py -i 1000 -r 5 -ni 500 data/input.tsv
```
![ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/4b36198a-e79a-4b12-bca2-bc18216041fd)

## How it works
The matching algorithm employs an evolutionary algorithm approach:

1. Generates random initial recommendations for each participant.
2. Evaluates solutions using a fitness function that rewards good matches and penalizes poor ones.
3. Iteratively improves the solution through mutation (randomly changing some recommendations) and selection (keeping better solutions).
4. Repeats for a set number of generations to optimize overall match quality.

### Input file
The input file provided to the algorithm contains a list of participants, each described by their unique ID, their possessed attributes, and the attributes they are seeking. The format of the file is as follows:

Each line represents a single participant.
- The line begins with a unique numerical ID.
- This is followed by the attributes the participant possesses.
- Finally, the attributes the participant is seeking are listed.

The fields are separated by a tab character (\t). 

Example:
```tsv
1    DEVELOPER    INVESTOR,DEVELOPER
2    INVESTOR     SALES,MARKETING
3    DEVELOPER    DEVELOPER,ARCHITECT
...
```

## Contributing
Before contributing to the project, please ensure that your code passes the following lint checks:
```bash
$ ruff check 
$ ruff format
```
