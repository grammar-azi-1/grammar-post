from django.urls import path
from grammars.api.views import RuleCategorysApiView, RuleCategoryUpdateApiView, RuleSubCategoryUpdateApiView, RuleSubCategoryApiView

urlpatterns = [

    path('rules/', RuleCategorysApiView.as_view(), name = 'rules'),
    path('rule/<int:pk>/', RuleCategoryUpdateApiView.as_view(), name = 'rule_update'),
    path('rules/subcategories/', RuleSubCategoryApiView.as_view(), name = 'subcategories'),
    path('rules/subcategory/<int:pk>/', RuleSubCategoryUpdateApiView.as_view(), name = 'subcategory_update'),
]