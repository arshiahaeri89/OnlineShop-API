from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .serializers import *
from .models import *


class ShopUserApiView(ModelViewSet):
    queryset = ShopUser.objects.all()
    serializer_class = ShopUserSerializer


class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductApiViewPagination(PageNumberPagination):
    page_size = 2  # TODO: Find a Good Page Size


class ProductApiView(ModelViewSet):
    queryset = Product.objects.order_by('-created_at').all()
    serializer_class = ProductSerializer
    pagination_class = ProductApiViewPagination


class ProductImageApiView(ModelViewSet):
    queryset = ProductImage.objects.order_by('image_number').all()
    serializer_class = ProductImageSerializer


class CommentApiViewPagination(PageNumberPagination):
    page_size = 2  # TODO: Find a Good Page Size


class CommentApiView(ModelViewSet):
    queryset = Comment.objects.order_by('-created_at').all()
    serializer_class = CommentSerializer
    pagination_class = CommentApiViewPagination
