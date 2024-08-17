# Conference Matchmaker

Conference Matchmaker is an intelligent system designed to enhance business conferences by helping participants establish valuable connections based on their skills and interests.

## Project Description

The system analyzes the attributes and preferences of conference participants to suggest the 5 most suitable people for each attendee to connect with. The goal is to maximize the value of interactions between participants by matching them based on their possessed and sought-after characteristics.

## Algorithm

The matching algorithm employs a genetic algorithm approach:

1. Generates random initial recommendations for each participant.
2. Evaluates solutions using a fitness function that rewards good matches and penalizes poor ones.
3. Iteratively improves the solution through mutation (randomly changing some recommendations) and selection (keeping better solutions).
4. Repeats for a set number of generations to optimize overall match quality.

This method aims to maximize meaningful connections among conference participants based on their attributes and preferences.

- Installing project dependencies 
```
pip install -r requirements.txt
```
- Running external scripts (ruff)
```
ruff check 
ruff format
```
- Example program execution
```
python src\main.py data\inputdata.txt
```
