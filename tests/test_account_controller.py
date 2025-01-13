import unittest
from unittest.mock import MagicMock
from SocialScores.Controllers.AccountController import AccountController


class TestAccountController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = AccountController(self.mock_db)

    def test_account_controller_instantiation(self):
        self.assertIsInstance(self.controller, AccountController)

    def test_get_account_by_id(self):
        mock_account = {"id": 1, "username": "test_user", "email": "test@test.com"}
        self.controller.repo.get_account_by_id = MagicMock(return_value=mock_account)

        result = self.controller.get_account_by_id(1)

        self.controller.repo.get_account_by_id.assert_called_once_with(1)
        self.assertEqual(result["username"], "test_user")
        self.assertEqual(result["email"], "test@test.com")

    def test_update_socialscore(self):
        mock_account = {"id": 1, "username": "test_user", "socialscore": 100}
        updated_account = {"id": 1, "username": "test_user", "socialscore": 110}

        self.controller.repo.update_socialscore = MagicMock(return_value=updated_account)

        result = self.controller.update_socialscore(account_id=1, delta=10)

        self.controller.repo.update_socialscore.assert_called_once_with(1, 10)

        self.assertEqual(result["socialscore"], 110)

if __name__ == "__main__":
    unittest.main()
