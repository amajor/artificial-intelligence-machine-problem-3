""" The unit tests for the GenGameBoard class. """
import unittest
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

    def test_pre_requisite(self):
        """ Tests the limitations constraints for prerequisite courses. """
        self.skipTest('Test not yet created.')

    def test_get_possible_course_list(self):
        """ Tests the course schedule generation. """
        self.skipTest('Test not yet created.')


if __name__ == '__main__':
    unittest.main()
