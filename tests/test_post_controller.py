import unittest
from unittest.mock import MagicMock
from SocialScores.Controllers.PostController import PostController
from SocialScores.Models.Post import PostBase


class TestPostController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = PostController(self.mock_db)

    def test_post_controller_instantiation(self):
        self.assertIsInstance(self.controller, PostController)

    def test_create_post(self):
        mock_post = PostBase(user="test_user", account_id=1, text="Test Post", image=None)
        self.controller.repo.create_post = MagicMock(
            return_value={"id": 1, "user": "test_user", "text": "Test Post"}
        )

        result = self.controller.create_post(
            user="test_user", account_id=1, text="Test Post", image=None
        )

        self.controller.repo.create_post.assert_called_once_with(
            user="test_user", account_id=1, text="Test Post", image_id=None
        )
        self.assertEqual(result["text"], "Test Post")

if __name__ == "__main__":
    unittest.main()
