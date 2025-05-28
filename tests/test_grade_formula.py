import pytest
from app.grade_formula import (
    calculate_inf_grade,
    calculate_cos_grade,
    calculate_adv_grade
)

def test_calculate_inf_grade():
    data = {
        'report_a': 20,       # out of 25
        'report_b': 16,       # out of 20
        'group_exercise': 4,  # out of 5
        'cla_scores': 9,      # out of 10
        'quiz_scores': 12     # out of 15
    }
    expected = round((20/25)*25 + (16/20)*20 + (4/5)*5 + (9/10)*30 + (12/15)*20, 2)
    assert calculate_inf_grade(data) == expected

def test_calculate_cos_grade():
    data = {
        'lab_exercises': 9,   # out of 10
        'assignment1': 80,    # out of 100
        'assignment2': 70,    # out of 100
        'midterm': 30         # out of 35
    }
    expected = round((9/10)*10 + (80/100)*30 + (70/100)*40 + (30/35)*20, 2)
    assert calculate_cos_grade(data) == expected

def test_calculate_adv_grade():
    data = {
        'quiz_scores': 16,     # out of 20
        'assignment1': 8,      # out of 10
        'assignment2': 35,     # out of 40
        'obow_test': 27        # out of 30
    }
    expected = round((16/20)*20 + (8/10)*10 + (35/40)*40 + (27/30)*30, 2)
    assert calculate_adv_grade(data) == expected
