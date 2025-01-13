import unittest
from unittest.mock import MagicMock, patch
from SocialScores.Controllers.ImageController import ImageController
from SocialScores.Models.Image import Image

class TestImageController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = ImageController(self.mock_db)

    def test_image_controller_instantiation(self):
        self.assertIsInstance(self.controller, ImageController)

    def test_add_image(self):
        fake_image = Image(filename="test.jpg", binary_data=b"binary_data", uploader="mark")
        self.controller.repo.add_image = MagicMock(return_value=fake_image)

        result = self.controller.add_image(filename="test.jpg", binary_data=b"binary_data", uploader="mark")

        self.assertEqual(result.filename, "test.jpg")
        self.assertEqual(result.uploader, "mark")
        self.assertIsInstance(result, Image)

    @patch("SocialScores.Database.RepositoryImage.RepositoryImage.get_image_by_id")
    def test_get_image_by_id(self, mock_get_image_by_id):
        fake_image = Image(filename="test.jpg", binary_data=b"binary_data", uploader="mark")
        mock_get_image_by_id.return_value = fake_image

        result = self.controller.get_image_by_id(1)

        self.assertEqual(result.filename, "test.jpg")
        self.assertEqual(result.uploader, "mark")
        self.assertIsInstance(result, Image)

if __name__ == "__main__":
    unittest.main()
