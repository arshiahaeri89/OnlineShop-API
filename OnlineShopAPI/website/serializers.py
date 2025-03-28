from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['role'] = self.user.role
        return data


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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # ***


class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    images = ProductImageSerializer(read_only=True, many=True)
    category_name = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    orders = OrderSerializer(read_only=True, many=True)

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
