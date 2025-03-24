from rest_framework import serializers

from .models import *


class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ['username', 'first_name', 'last_name',
                  'phone_number', 'address', 'postal_code']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=ShopUser.objects.all())

    class Meta:
        model = Comment
        fields = ['product', 'user', 'title', 'text', 'rate']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'image_number', 'product']


class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    images = ProductImageSerializer(read_only=True, many=True)
    category_name = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def get_category_name(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = '__all__'
