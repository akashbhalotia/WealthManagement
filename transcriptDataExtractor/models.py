from django.db import models
from django.core.validators import FileExtensionValidator
from .validators import validate_file_size, validate_file_extension


class Transcript(models.Model):
    """
    Model representing a transcript.
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default='No Title')
    file = models.FileField(upload_to='uploads/',
                            validators=[FileExtensionValidator(allowed_extensions=['txt']), validate_file_size],
                            null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now=True)

    assets = models.TextField(editable=False)
    expenditures = models.TextField(editable=False)
    income = models.TextField(editable=False)

    def clean(self):
        if self.file:
            validate_file_size(self.file)
            validate_file_extension(self.file)

    def __str__(self):
        return self.title
