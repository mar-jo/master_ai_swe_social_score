import unittest
from unittest.mock import MagicMock, patch
from SocialScores.Controllers.ImageController import ImageController
from SocialScores.Database.RepositoryImage import RepositoryImage
from SocialScores.Models.Image import Image

class TestImageController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.repo = MagicMock(spec=RepositoryImage)
        self.controller = ImageController(self.mock_db)

    def test_image_controller_instantiation(self):
        self.assertIsInstance(self.controller, ImageController)

    @patch('pika.BlockingConnection')
    def test_add_image(self, mock_blocking_connection):
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_blocking_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        image = self.controller.add_image(filename="test.jpg", binary_data=b"binary_data", uploader="mark")

        mock_connection.channel.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue='resize_queue')
        mock_channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='resize_queue',
            body=str(image.id)
        )

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
