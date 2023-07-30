
import unittest
from unittest.mock import patch
from my_module import get_logger


class TestGetLogger(unittest.TestCase):

    @patch('my_module.getLogger')
    @patch('my_module.logging.basicConfig')
    def test_get_logger(self, mock_basic_config, mock_get_logger):
        # Set up
        debug = True

        # Call the function under test
        result = get_logger(debug)

        # Assertions
        mock_basic_config.assert_called_once_with(format="%(asctime)s %(levelname)s - %(message)s")
        mock_get_logger.assert_called_once_with(__name__)
        self.assertEqual(result, mock_get_logger.return_value)
        self.assertEqual(result.level, mock_get_logger.return_value.setLevel.return_value)


if __name__ == '__main__':
    unittest.main()
