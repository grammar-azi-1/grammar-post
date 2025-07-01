from grammars.models import RuleCategory, RuleSubCategory
from django.http import JsonResponse
from grammars.api.serializers import RuleCategorySerializer, RuleSubCategorySerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter
from grammars.filters import RuleCatFilter, HiglightFilter

# def rules(request):
#     rules = Rule.objects.all()
#     serializer = RuleSerializer(rules, many = True)
#     # rule_dict = []
#     # for rule in rules:
#     #     rule_dict.append({
#     #         'id': rule.id,
#     #         'title': rule.title
#     #     })

#     return JsonResponse(data=serializer.data, safe=False)

# class RulesApiView(ListCreateAPIView):
#     serializer_class = RuleSerializer
#     queryset = Rule.objects.all()
#     permission_classes = [IsAuthenticatedOrReadOnly,]

# class RuleUpdateApiView(RetrieveUpdateDestroyAPIView):
#     serializer_class = RuleSerializer
#     queryset = Rule.objects.all()

class RuleCategorysApiView(ListCreateAPIView):
    serializer_class = RuleCategorySerializer
    queryset = RuleCategory.objects.all()
    filter_backends = (RuleCatFilter, SearchFilter, HiglightFilter,)
    search_fields = ('subcategories__content',)


class RuleCategoryUpdateApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = RuleCategorySerializer
    queryset = RuleCategory.objects.all()

class RuleSubCategoryApiView(ListCreateAPIView):
    serializer_class = RuleSubCategorySerializer
    queryset = RuleSubCategory.objects.all()

class RuleSubCategoryUpdateApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = RuleSubCategorySerializer
    queryset = RuleSubCategory.objects.all()