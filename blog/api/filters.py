from rest_framework.filters import BaseFilterBackend

class LimitFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get('limit')

        if limit and limit.isdigit():
            return queryset[:int(limit)]
        
        return queryset