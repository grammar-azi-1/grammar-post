from rest_framework import serializers
from grammars.models import RuleCategory, RuleSubCategory
from grammars.api.utils import higlight

class RuleSubCategorySerializer(serializers.ModelSerializer):

    content = serializers.SerializerMethodField()

    class Meta:
        model = RuleSubCategory
        fields = (
            'id',
            'category_id',
            'title',
            'content',
        )

    def get_content(self, obj):
        request = self.context.get('request')
        term = getattr(request, '_search_term', '')
        return higlight(obj.content, term)


class RuleCategorySerializer(serializers.ModelSerializer):
    subcategories = RuleSubCategorySerializer(many = True, read_only = True)
    class Meta:
        model = RuleCategory
        fields = (
            'id',
            'title',
            'subcategories'
        )



# class RuleSerializer(serializers.ModelSerializer):

#     category = RuleCategorySerializer()

#     class Meta:
#         model = Rule
#         fields = (
#             'id',
#             'title',
#             'category',
#             'description',
#         )


