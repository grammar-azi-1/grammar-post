from django.db import models
from core.models import AbstractModel
# Create your models here.

class RuleCategory(AbstractModel):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title    
    
    class Meta:
        verbose_name_plural = 'Rule Categories'

class RuleSubCategory(AbstractModel):
    category_id = models.ForeignKey(RuleCategory, related_name='subcategories', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title    
    
    class Meta:
        verbose_name_plural = 'Rule SubCategories'

# class Rule(AbstractModel):
#     subcategory = models.ForeignKey(RuleSubCategory, related_name='rule', on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     description = models.TextField()

#     def __str__(self):
#         if self.category:
#             return f'{self.category} - {self.title}'
#         return self.title