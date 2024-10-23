from base import UnitScores
from cli import choose_one, yes_or_no, enter_str, enter_float


UNIT_SCORES_MIN = 16
UNIT_SCORES_MAX = 30

MARK_MIN = 0.0
MARK_MAX = 100.0

UNIT_CODE_LENGTH = 7

def enter_unit_score():
    print('Enter unit code')
    unit = enter_str(7,7)
    print('Enter score for',unit)
    score = enter_float(MARK_MIN,MARK_MAX)
    return unit, score

def collect_unit_scores():
    print('Please enter your unit scores')
    unit_scores:UnitScores=list()

    while len(unit_scores)<=UNIT_SCORES_MAX:
        unit_score = enter_unit_score()
        unit_scores.append(unit_score)
        if not yes_or_no('Do you want to continue'):
            break

    return unit_scores


import xmlrpc.client as client

proxy = client.ServerProxy('http://localhost:5000/RPC2')

print(proxy.student_assessment(20241201,'Jim'))
