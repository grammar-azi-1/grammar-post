from django.core.exceptions import ValidationError
import os 

def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File is too large, size should be under 5 MB')
    
def validate_file_type(value):
    typefile = os.path.splitext(value.name)[1].lower()
    print(typefile)
    allowed_extensions = ['.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg']
    if typefile not in allowed_extensions:
        raise ValidationError('Wrong file type! Allowed file types are: PDF, DOCX, TXT, PNG, JPG')