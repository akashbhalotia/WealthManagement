from .models import Transcript
from .serializers import TranscriptSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .utils import extract_with_timeout
from concurrent.futures import TimeoutError


class TranscriptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that enables CRUD operations on Transcripts.
    """

    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer

    def perform_create(self, serializer):
        self.process_transcript_and_update(serializer)

    def perform_update(self, serializer):
        self.process_transcript_and_update(serializer)

    def process_transcript_and_update(self, serializer):
        instance = serializer.save()

        # Ensure there is a file before attempting to process
        if not instance.file:
            raise ValueError("File is missing for this instance.")

        # Extract financial data from the transcript file
        try:
            extracted_data = extract_with_timeout(instance.file.path, timeout=10)
            self.set_financial_data(instance, extracted_data)
        except TimeoutError as timeout_error:
            self.handle_timeout(instance)
            raise timeout_error
        except (FileNotFoundError, EnvironmentError, RuntimeError) as error:
            raise error
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(response.data, status=status.HTTP_201_CREATED)
        except TimeoutError as timeout_error:
            return Response(
                {
                    "detail": str(timeout_error),
                    "note": "The instance has been created, but the data extraction timed out. You can update the file to retry.",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(response.data, status=status.HTTP_200_OK)
        except TimeoutError as timeout_error:
            return Response(
                {
                    "detail": str(timeout_error),
                    "note": "The instance has been updated, but the data extraction timed out. You can update the file to retry.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def set_financial_data(self, instance, extracted_data):
        """
        Saves asset, expenditure and income information.
        """

        insufficient_data_message = "Not enough data."

        instance.assets = extracted_data.assets if len(extracted_data.assets) > 0 else [insufficient_data_message]
        instance.expenditures = extracted_data.expenditures if len(extracted_data.expenditures) > 0 else [
            insufficient_data_message]
        instance.income = extracted_data.income if len(extracted_data.income) > 0 else [insufficient_data_message]
        instance.save()

    def handle_timeout(self, instance):
        """
        Saves the instance and includes a message indicating that extraction timed out.
        """

        timeout_message = "Extraction timed out. Please try again later."

        instance.assets = [timeout_message]
        instance.expenditures = [timeout_message]
        instance.income = [timeout_message]
        instance.save()
