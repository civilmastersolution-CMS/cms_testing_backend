from rest_framework import serializers
from .models import Partnership, Customership, Product, RequestForm, ProjectReference, News

class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = '__all__'

class CustomershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customership
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class RequestFormSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    class Meta:
        model = RequestForm
        fields = '__all__'

class ProjectReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReference
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'