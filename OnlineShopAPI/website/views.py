from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .serializers import *
from .models import *


class ShopUserApiView(ModelViewSet):
    queryset = ShopUser.objects.all()
    serializer_class = ShopUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ShopUser.objects.filter(id=int(self.request.user.id))

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


class CategoryApiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductApiViewPagination(PageNumberPagination):
    page_size = 50


class ProductApiView(ModelViewSet):
    queryset = Product.objects.order_by('-created_at').all()
    serializer_class = ProductSerializer
    pagination_class = ProductApiViewPagination
    permission_classes = [AllowAny]


class ProductImageApiView(ModelViewSet):
    queryset = ProductImage.objects.order_by('image_number').all()
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]


class CommentApiViewPagination(PageNumberPagination):
    page_size = 10


class CommentApiView(ModelViewSet):
    queryset = Comment.objects.order_by('-created_at').all()
    serializer_class = CommentSerializer
    pagination_class = CommentApiViewPagination
    permission_classes = [AllowAny]


class OrderApiView(ModelViewSet):
    queryset = Order.objects.order_by('-created_at').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Validate that the user creating the order is the authenticated user
        if 'user' in self.request.data and int(self.request.data['user']) != self.request.user.id:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        # Save the order with the authenticated user
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Ensure the user trying to update the order owns it
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        # Proceed with the update
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        # If the user is authenticated, filter orders specific to the user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()  # Return empty queryset for unauthenticated users
