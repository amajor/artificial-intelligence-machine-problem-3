"""
Alison Major
October 5, 2021
Artificial Intelligence 1 – CPSC 57100
Fall Semester 2021
Machine Problem 3

Full code and test suite available on GitHub:
https://github.com/amajor/artificial-intelligence-machine-problem-3

Program checks if there are possible schedules for students for a given
start term and finish term, given all constraints.
This works by mapping a term number to each course, given all constraints.
It assigns a negative term number if course is not taken (e.g. elective that is not needed)

ASSUMPTION: term numbers start with 1
"""
import pandas as pd
# import numpy as np
from constraint import Problem


def create_term_list(terms, years=4):
    """ Create a list of term indexes for years in the future. """
    all_terms = []
    for year in range(years):
        for term in terms:
            all_terms.append(year * 6 + term)
    return all_terms


def map_to_term_label(term_num):
    """ Returns the label of a term, given its number. """
    term_num_to_label_map = {
        0: 'Fall 1',
        1: 'Fall 2',
        2: 'Spring 1',
        3: 'Spring 2',
        4: 'Summer 1',
        5: 'Summer 2',
    }
    term_label = term_num_to_label_map[(term_num - 1) % 6]
    year = str((term_num - 1) // 6 + 1)

    if term_num < 1:
        return 'Not Taken'
    return 'Year ' + year + ' ' + term_label


def pre_requisite(prerequisite_course, other_course):
    """ Used for encoding prerequisite constraints, a is a prerequisite for b. """
    if prerequisite_course > 0 and other_course > 0:
        # Taking both pre-req course and other course
        return prerequisite_course < other_course
    if prerequisite_course > 0 > other_course:
        # Taking pre-req course, but not other course
        return True
    if prerequisite_course < 0 < other_course:
        # Taking other course, but not pre-req course
        return False
    return True  # Not taking pre-req a or course b


def get_possible_course_list(start_term, finish_term):
    """ Returns a possible course schedule,
        assuming student starts in start_term
        and finishes in finish_term. """
    print('\nstart_term: ', start_term)
    print('finish_term: ', finish_term, '\n')
    problem = Problem()

    # Read course_offerings file
    course_offerings = pd.read_excel('csp_course_rotations.xlsx', sheet_name='course_rotations')
    # course_prereqs = pd.read_excel('csp_course_rotations.xlsx', sheet_name='prereqs')

    # Foundation course terms
    foundation_courses = course_offerings[course_offerings.Type == 'foundation']
    for r, row in foundation_courses.iterrows():
        print('--> r:   ', r)
        print('--> row: ', row)
        problem.addVariable(row.Course, create_term_list(list(row[row == 1].index)))

    # TODO: Start Here
    # Core course terms

    # CS Electives course terms (-x = elective not taken)

    # Capstone

    # Guarantee no repeats of courses

    # Control start and finish terms

    # Control electives - exactly 3 courses must be chosen

    # Pre-reqs

    # TODO: End Here

    # Generate a possible solution
    sol = problem.getSolutions()
    print(len(sol))
    solutions = pd.Series(sol[0])
    return solutions.sort_values().map(map_to_term_label)


# Print heading
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: [put your name here]")

# Check for possible schedules for all start terms
for start in [1]:
    print('START TERM = ' + map_to_term_label(start))
    s = get_possible_course_list(start, start + 13)
    if s.empty:
        print('NO POSSIBLE SCHEDULE!')
    else:
        s2 = pd.Series(s.index.values, index=s)
        print(s2.to_string())
    print()
