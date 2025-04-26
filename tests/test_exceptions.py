import unittest
from awslogs.exceptions import (
    BaseAWSLogsException, 
    UnknownDateError, 
    TooManyStreamsFilteredError, 
    NoStreamsFilteredError
)

class TestExceptions(unittest.TestCase):
    def test_base_exception(self):
        exception = BaseAWSLogsException()
        self.assertEqual(exception.code, 1)
        self.assertEqual(exception.hint(), "Unknown Error.")
    
    def test_unknown_date_error(self):
        date_string = "invalid-date"
        exception = UnknownDateError(date_string)
        self.assertEqual(exception.code, 3)
        self.assertEqual(
            exception.hint(),
            "awslogs doesn't understand '{}' as a date.".format(date_string)
        )
    
    def test_too_many_streams_filtered_error(self):
        pattern = "test-pattern"
        count = 500
        limit = 100
        exception = TooManyStreamsFilteredError(pattern, count, limit)
        self.assertEqual(exception.code, 6)
        hint = exception.hint()
        self.assertIn(pattern, hint)
        self.assertIn(str(count), hint)
        self.assertIn(str(limit), hint)
    
    def test_no_streams_filtered_error(self):
        pattern = "non-existent-pattern"
        exception = NoStreamsFilteredError(pattern)
        self.assertEqual(exception.code, 7)
        self.assertIn(pattern, exception.hint())

if __name__ == '__main__':
    unittest.main() 