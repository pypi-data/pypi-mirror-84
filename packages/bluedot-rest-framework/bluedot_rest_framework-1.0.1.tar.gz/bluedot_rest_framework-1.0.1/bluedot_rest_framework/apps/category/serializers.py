from project.utils.serializers import CustomSerializer
from .models import Category


class CategorySerializer(CustomSerializer):

    class Meta:
        model = Category
        fields = '__all__'
