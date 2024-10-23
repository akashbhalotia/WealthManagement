from django.test import TestCase
from .models import Transcript
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


class TranscriptTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_upload_file_success(self):
        # Create a mock file
        mock_file = SimpleUploadedFile(
            "testfile.txt",  # Name of the file
            b"File content",  # Content of the file as bytes
            content_type="text/plain"
        )
        data = {
            "title": "Test File",
            "file": mock_file
        }

        response = self.client.post('/api/transcripts/', data, format="multipart")
        self.assertEqual(response.status_code, 201)

    def test_upload_pdf_error(self):
        mock_pdf = SimpleUploadedFile(
            "testfile.pdf",  # Name of the file
            b"%PDF-1.4 content",  # Content of the file mimicking a PDF
            content_type="application/pdf"
        )
        data = {
            "title": "Test PDF File",
            "file": mock_pdf
        }

        response = self.client.post('/api/transcripts/', data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is not allowed. Allowed extensions are: txt.', response.data['detail'])

    def test_upload_largeFile_error(self):
        large_file_content = b"x" * (1001 * 1024)  # Create a file of size 1001 KB
        mock_large_file = SimpleUploadedFile(
            "large_testfile.txt",  # Name of the file
            large_file_content,  # Content of the file
            content_type="text/plain"
        )
        data = {
            "title": "Large Test File",
            "file": mock_large_file
        }

        response = self.client.post('/api/transcripts/', data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Maximum file size is 1000KB.', response.data['detail'])
