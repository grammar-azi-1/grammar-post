from rest_framework.filters import SearchFilter
from grammars.models import RuleCategory
from django.core.exceptions import ValidationError

class RuleCatFilter(SearchFilter):
    min_limit = 3

    def get_search_terms(self, request):
        params = super().get_search_terms(request)

        for term in params:
            if len(term) < self.min_limit:
                raise ValidationError(f"Search term '{term}' exceeds min length of {self.min_limit} characters.")
            
        return params
    
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get('search', '')

        if not search_term.strip():
            return super().filter_queryset(request, queryset, view)
        symbols = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '[', ']', ';', "'", ':', '<', ',', '.', '>', '/', '\\', '|', '-', '+', '*', '/', '=', '_']
        count = 0
        for i in search_term:
            if i in symbols:
                count += 1

        if count == len(search_term):
            raise ValidationError(f"Search term '{search_term}' can not only consists of symbols.")
        
        return super().filter_queryset(request, queryset, view)


class HiglightFilter(SearchFilter):
    def get_search_terms(self, request):
        terms = super().get_search_terms(request)
        request._search_term = terms[0] if terms else ''
        return terms