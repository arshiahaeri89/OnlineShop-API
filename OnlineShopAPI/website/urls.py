from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('users', ShopUserApiView)
router.register('categories', CategoryApiView)
router.register('products', ProductApiView)
router.register('product_images', ProductImageApiView)
router.register('product_comments', CommentApiView)

app_name = 'website'
urlpatterns = [
    path('', include(router.urls))
]
