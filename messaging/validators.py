import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg',
                        '.png', '.pdf', '.doc', '.docx', '.gif', 'mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB limit
        raise ValidationError("File size cannot exceed 10MB")
