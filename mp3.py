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
from constraint import Problem, AllDifferentConstraint, SomeInSetConstraint


def create_term_list(terms, years=4):
    """ Create a list of term indexes for years in the future. """
    all_terms = []
    for year in range(years):
        for term in terms:
            all_terms.append(year * 6 + term)
    return all_terms


def remove_terms_beyond_finish(all_terms, finish_term):
    """ Remove all terms that are beyond the finish term. """
    return [x for x in all_terms if x <= finish_term]


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


def prerequisite(prereq_course_term, other_course_term):
    """ Used for encoding prerequisite constraints, a is a prerequisite for b. """
    if prereq_course_term > 0 and other_course_term > 0:
        # Taking both pre-req course and other course
        return prereq_course_term < other_course_term
    if prereq_course_term > 0 > other_course_term:
        # Taking pre-req course, but not other course
        return True
    if prereq_course_term < 0 < other_course_term:
        # Taking other course, but not pre-req course
        return False

    # Not taking pre-req course or other course
    return True


def add_courses_to_problem_by_filter(filter_term, course_offerings, finish_term, problem):
    """ Adds the courses to the problem by filtering based on the term. """
    for _row_num, row in course_offerings[course_offerings.Type == filter_term].iterrows():
        # Capture course information
        course_label = row.Course
        course_available_terms = create_term_list(list(row[row == 1].index))

        # Remove terms beyond the Finish Term
        course_available_terms = remove_terms_beyond_finish(course_available_terms, finish_term)

        # Add the variable to the problem
        problem.addVariable(course_label, course_available_terms)


def get_possible_course_list(start_term, finish_term):
    """ Returns a possible course schedule,
        assuming student starts in start_term
        and finishes in finish_term. """
    problem = Problem()

    # Read course_offerings file
    course_offerings = pd.read_excel('csp_course_rotations.xlsx', sheet_name='course_rotations')
    course_prerequisites = pd.read_excel('csp_course_rotations.xlsx', sheet_name='prereqs')

    # Foundation course terms
    add_courses_to_problem_by_filter('foundation', course_offerings, finish_term, problem)

    # Core course terms
    add_courses_to_problem_by_filter('core', course_offerings, finish_term, problem)

    # CS Electives course terms (-x = elective not taken)
    negative_elective_terms = []
    elective_courses = course_offerings[course_offerings.Type == 'elective']
    for row_num, row in elective_courses.iterrows():
        # Capture course information
        course_label = row.Course
        course_available_terms = create_term_list(list(row[row == 1].index)) + [-row_num]

        # Remove terms beyond the Finish Term
        course_available_terms = remove_terms_beyond_finish(course_available_terms, finish_term)

        # Add the variable to the problem
        problem.addVariable(course_label, course_available_terms)

        # Keep track of the negative terms for electives to use later
        negative_elective_terms.append(-row_num)

    # Capstone
    add_courses_to_problem_by_filter('capstone', course_offerings, finish_term, problem)

    # Guarantee no repeats of courses and only once course per term
    problem.addConstraint(AllDifferentConstraint())

    # Control start and finish terms
    problem.addConstraint(SomeInSetConstraint([start_term]))
    problem.addConstraint(SomeInSetConstraint([finish_term]))

    # Control electives - exactly 3 courses must be chosen
    number_of_electives_ignored = len(elective_courses) - 3
    problem.addConstraint(
        SomeInSetConstraint(negative_elective_terms, n=number_of_electives_ignored, exact=True)
    )

    # Set constraints for the Pre-requisites.
    row_num = 0
    while row_num < len(course_prerequisites):
        problem.addConstraint(prerequisite, [
            course_prerequisites.iloc[row_num]['prereq'],  # the prerequisite course
            course_prerequisites.iloc[row_num]['course']  # the other course
        ])
        row_num += 1

    # Generate a possible solution
    sol = problem.getSolutions()

    # Print number of solutions
    print('Number of Possible Degree Plans is', len(sol))

    # Return the top solution
    solutions = pd.Series(sol[0])
    return solutions.sort_values().map(map_to_term_label)


def main():
    """ Runs the main program for the course planning. """

    # Print out the header info
    print('CLASS: Artificial Intelligence, Lewis University')
    print('MP3: Course Planning using a Constraint Satisfaction Problem Formulation')
    print('SEMESTER: FALL 2021, TERM 1')
    print('NAME: ALISON MAJOR\n')

    # Check for possible schedules for all start terms
    for start in [1]:
        finish = start + 13
        print('START TERM  = ' + map_to_term_label(start))
        print('FINISH TERM = ' + map_to_term_label(finish))
        solution_1 = get_possible_course_list(start, finish)
        if solution_1.empty:
            print('\nNO POSSIBLE SCHEDULE!')
        else:
            solution_2 = pd.Series(solution_1.index.values, index=solution_1)
            print('\nSample Degree Plan')
            print(solution_2.to_string())
        print()


if __name__ == "__main__":
    main()
