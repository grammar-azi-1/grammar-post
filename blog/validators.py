from django.core.exceptions import ValidationError
import os


def validate_file_type(value):
    typefile = os.path.splitext(value.name)[1].lower()
    print(typefile)
    allowed_extensions =[".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".webp", ".heic", ".heif", ".avif", ".svg", ".ico", ".raw",
    ".psd", ".ai", ".eps", ".indd"]

    if typefile not in allowed_extensions:
        raise ValidationError('Wrong file type! Must use any of these formats : ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",".webp", ".heic", ".heif", ".avif", ".svg", ".ico", ".raw",".psd", ".ai", ".eps", ".indd"')