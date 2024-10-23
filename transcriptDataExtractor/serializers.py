from rest_framework import serializers
from .models import Transcript
from .validators import validate_file_size, validate_file_extension


class TranscriptSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Transcript.
    """

    class Meta:
        model = Transcript
        fields = ['id', 'title', 'file', 'assets', 'expenditures', 'income', 'uploaded_at']
        read_only_fields = ['assets', 'expenditures', 'income', 'uploaded_at']
        extra_kwargs = {
            'file': {'required': False}  # Make the file field optional during update
        }

    def validate(self, data):
        if not self.instance and not data.get('file'):
            raise serializers.ValidationError({"file": "This field is required when creating a new instance."})
        return data

    def validate_file(self, file):
        validate_file_size(file)
        validate_file_extension(file)

        return file
