from django.core.exceptions import ValidationError


def validate_file_size(file):
    """
    Checks if the uploaded file is within allowed file size.
    """

    max_size_kb = 1000  # maximum size in kilobytes
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"Maximum file size is {max_size_kb}KB.")


def validate_file_extension(file):
    """
    Checks if the uploaded file is a .txt file.
    """

    allowed_extension = '.txt'
    if not file.name.endswith(allowed_extension):
        raise ValidationError(f"Unsupported file extension. Only .txt files are allowed.")
