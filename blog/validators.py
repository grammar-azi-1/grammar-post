from django.core.exceptions import ValidationError
import os


def validate_file_type(value):
    typefile = os.path.splitext(value.name)[1].lower()
    print(typefile)
    allowed_extensions = ['.png', '.jpg']
    if typefile not in allowed_extensions:
        raise ValidationError('Wrong file type! Allowed file types are: PDF, DOCX, TXT, PNG, JPG')