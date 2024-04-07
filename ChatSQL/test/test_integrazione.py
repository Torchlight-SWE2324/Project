import sys
import unittest
from unittest.mock import Mock
sys.path.append('ChatSQL')
from model import *
from widgets import *
from controller import *


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.model = AuthenticationService()
        self.view = Mock(spec=LoginWidget)
        self.controller = AuthenticationController(self.model, self.view)

    def test_successful_login(self):
        # Set up mock input
        self.view.get_username = "admin"
        self.view.get_password = "admin"

        # Set up model to return True for successful login
        self.model.check_login = True

        # Call the operation_login method
        self.controller.operation_login()

        # Check if positive_login_outcome method is called
        self.view.positive_login_outcome.assert_called_once()

    def test_failed_login(self):
        # Set up mock input
        self.view.get_username = "test_user"
        self.view.get_password = "wrong_password"

        # Set up model to return False for failed login
        self.model.check_login = False

        # Call the operation_login method
        self.controller.operation_login()

        # Check if negative_login_outcome method is called
        self.view.negative_login_outcome.assert_called_once()

    def test_missing_credentials(self):
        # Set up mock input
        self.view.get_username = ""
        self.view.get_password = "test_password"

        # Call the operation_login method
        self.controller.operation_login()

        # Check if missing_credential_outcome method is called
        self.view.missing_credential_outcome.assert_called_once()

if __name__ == '__main__':
    unittest.main()

