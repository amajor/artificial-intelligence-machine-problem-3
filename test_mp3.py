""" The unit tests for the GenGameBoard class. """
import unittest
from parameterized import parameterized

import mp3


class TestCoursePlanning(unittest.TestCase):
    """ Will run tests against modules and functions used for course planning. """

    def test_create_term_list(self):
        """ Tests the creation of a list of term indexes for years in the future. """
        self.skipTest('Test not yet created.')

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
