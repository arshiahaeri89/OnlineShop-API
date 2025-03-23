from rest_framework import serializers

from .models import *


class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = ShopUserSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    images = ProductImageSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'
