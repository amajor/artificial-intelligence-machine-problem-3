""" The unit tests for the GenGameBoard class. """
import io
import sys
import unittest

from constraint import Problem
from parameterized import parameterized

import mp3


class TestCoursePlanning(unittest.TestCase):
    """ Will run tests against modules and functions used for course planning. """

    @parameterized.expand([
        (
            'Fall and Spring only for 3 years',
            [0, 1, 2, 3],  # desired terms
            3,             # desired years
            [0, 1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15]
        ), (
            'All terms only for 2 years',
            [0, 1, 2, 3, 4, 5],  # desired terms
            2,                   # desired years
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        ), (
            'Start in spring, only Spring & Fall',
            [2, 3, 6, 7],  # desired terms
            4,             # desired years
            [2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 18, 19, 20, 21, 24, 25]
        )
    ])
    def test_create_term_list(self, _test_name, desired_terms, desired_years, expected_list):
        """ Tests the creation of a list of term indexes for years in the future. """
        actual_list = mp3.create_term_list(desired_terms, desired_years)
        self.assertEqual(expected_list, actual_list)

    @parameterized.expand([
        ('Term number 0 is "Not Taken"', 0, 'Not Taken'),
        ('Term number 1 is "Year 1 Fall 1"', 1, 'Year 1 Fall 1'),
        ('Term number 2 is "Year 1 Fall 2"', 2, 'Year 1 Fall 2'),
        ('Term number 3 is "Year 1 Spring 1"', 3, 'Year 1 Spring 1'),
        ('Term number 4 is "Year 1 Spring 2"', 4, 'Year 1 Spring 2'),
        ('Term number 5 is "Year 1 Summer 1"', 5, 'Year 1 Summer 1'),
        ('Term number 6 is "Year 1 Summer 2"', 6, 'Year 1 Summer 2'),
        ('Term number 13 is "Year 3 Fall 1"', 13, 'Year 3 Fall 1'),
    ])
    def test_map_to_term_label(self, _test_name, term_number, expected_label):
        """ Tests mapping the term number to its label. """
        actual_label = mp3.map_to_term_label(term_number)
        self.assertEqual(expected_label, actual_label)

    @parameterized.expand([
        ('Taking first pre-req, then course', 1, 2, True),
        ('Taking first course, then pre-req', 3, 2, False),
        ('Taking pre-req, not other course', 1, -1, True),
        ('Taking other course, not pre-req', -1, 1, False),
        ('Not taking pre-req or other course', 0, 0, True)
    ])
    def test_prerequisite_basic(self, _test_name, taking_prerequisite, taking_course, expected):
        """ Tests the limitations constraints for prerequisite courses. """
        actual = mp3.prerequisite(taking_prerequisite, taking_course)
        self.assertEqual(expected, actual)

    def test_prerequisite(self):
        """ Tests the prerequisite as a constraint when solving a problem. """
        problem = Problem()
        problem.addVariable("Course1", [2, 4, 5])
        problem.addVariable("Course2", [1, 3, 6])

        # We treat Course1 as a prereq for Course2
        problem.addConstraint(mp3.prerequisite, ["Course1", "Course2"])
        expected = [
            {'Course1': 5, 'Course2': 6},
            {'Course1': 4, 'Course2': 6},
            {'Course1': 2, 'Course2': 3},
            {'Course1': 2, 'Course2': 6}
        ]
        actual = problem.getSolutions()
        self.assertEqual(expected, actual)

    @parameterized.expand([
        ('All terms greater than 5 are removed', [1, 3, 5, 7, 9], 5, [1, 3, 5]),
        ('All terms greater than 2 are removed', [2, 1, 9, 5, 3, 7], 2, [2, 1]),
    ])
    def test_remove_terms_beyond_finish(self, _test_name, all_terms, finish_term, expected):
        """ Tests that we remove any terms beyond our finish. """
        actual = mp3.remove_terms_beyond_finish(all_terms, finish_term)
        self.assertEqual(expected, actual)

    def test_get_possible_course_list(self):
        """ Test the possible course list output based on hard-coded file. """
        # Create the path and capture the output.
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # and redirect stdout.

        # Run the main program.
        mp3.main()

        # Confirm printing of correct START_TERM.
        expected_start_term_msg = 'START TERM  = Year 1 Fall 1'
        self.assertIn(expected_start_term_msg, captured_output.getvalue())

        # Confirm the expected sample output.
        expected_course_plan = '''START TERM  = Year 1 Fall 1
FINISH TERM = Year 3 Fall 2
Number of Possible Degree Plans is 9488

Sample Degree Plan
Not Taken          CPSC-57400
Not Taken          CPSC-57200
Not Taken          CPSC-57100
Not Taken          CPSC-55200
Not Taken          CPSC-51700
Year 1 Fall 1      CPSC-50600
Year 1 Fall 2      MATH-51100
Year 1 Spring 1    MATH-51000
Year 1 Spring 2    MATH-51200
Year 1 Summer 1    CPSC-50100
Year 2 Fall 1      CPSC-51100
Year 2 Fall 2      CPSC-53000
Year 2 Spring 1    CPSC-54000
Year 2 Spring 2    CPSC-55500
Year 2 Summer 1    CPSC-51000
Year 2 Summer 2    CPSC-52500
Year 3 Fall 1      CPSC-55000
Year 3 Fall 2      CPSC-59000'''
        self.assertIn(expected_course_plan, captured_output.getvalue())

    def test_get_possible_course_list_no_repeats(self):
        """ Tests the courses are not repeated and only 1 course per term. """
        self.skipTest('Need to allow for file input to control test data.')

    def test_get_possible_course_list_start_term(self):
        """ Tests the input start term is included in final solution. """
        self.skipTest('No test written; see general test for get_possible_course_list')

    def test_get_possible_course_list_finish_term(self):
        """ Tests the input start term is included in final solution. """
        self.skipTest('No test written; see general test for get_possible_course_list')

    def test_get_possible_course_list_number_of_electives(self):
        """ Tests that only 3 electives are added to the plan. """
        self.skipTest('No test written; see general test for get_possible_course_list')

    def test_get_possible_course_list_prerequisites(self):
        """ Tests that the plan is limited by prerequisite courses. """
        self.skipTest('No test written; see general test for get_possible_course_list')


if __name__ == '__main__':
    unittest.main()
