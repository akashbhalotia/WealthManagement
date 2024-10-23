from django.test import TestCase
from .models import Transcript
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


class TranscriptTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some test transcript objects
        cls.transcript1 = Transcript.objects.create(
            title="Transcript 1",
            file=SimpleUploadedFile("file1.txt",
                                    b"Content of file 1. Jack earns Rs. 50,000 per month. His expenses are Rs. 10,000 per month. He has a house and a car.",
                                    content_type="text/plain")
        )
        cls.transcript2 = Transcript.objects.create(
            title="Transcript 2",
            file=SimpleUploadedFile("file2.txt", b"Content of file 2", content_type="text/plain")
        )

    def test_get_transcripts_list(self):
        # Perform GET request to the transcripts list endpoint
        response = self.client.get('/api/transcripts/', format="json")

        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # If the response is paginated, we need to access the 'results' key
        if 'results' in response.data:
            transcripts = response.data['results']
        else:
            transcripts = response.data

        # Filter the transcripts based on the titles created
        filtered_transcripts = [t for t in transcripts if t['title'] in ["Transcript 1", "Transcript 2"]]

        # Check that the response contains the correct number of transcripts
        self.assertEqual(len(filtered_transcripts), 2)

        # Check that the titles of the transcripts match
        self.assertEqual(filtered_transcripts[0]['title'], self.transcript1.title)
        self.assertEqual(filtered_transcripts[1]['title'], self.transcript2.title)

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
