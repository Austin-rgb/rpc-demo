from server1 import evaluate
from random import randint

def generate_scores():
    unit_scores = []
    for i in range(25):
        unit_scores.append((f'ccs110{i}',randint(30,100)))

    return unit_scores

for i in  range(10):
    print(evaluate(generate_scores(),'user123'))