from django.template import Library
register = Library()
from grammars.models import RuleCategory

@register.simple_tag
def get_categories():
    return RuleCategory.objects.filter(parent = None)
