from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import *


class ShopUserApiView(ModelViewSet):
    queryset = ShopUser.objects.all()
    serializer_class = ShopUserSerializer


class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageApiView(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class CommentApiView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
