from django.db import models
from core.validators import validate_file_size, validate_file_type
import os
# Create your models here.

class AbstractModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Check_up(AbstractModel):
    file = models.FileField(upload_to='uploads/', validators=[validate_file_size, validate_file_type])
    comment = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=13)
    accept_policy = models.BooleanField(default=False)

    def __str__(self):
        return self.comment 
    