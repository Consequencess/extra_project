from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductAPIView, CategoryAPIView, get_hello

router = DefaultRouter()
router.register('category', CategoryAPIView)
router.register('', ProductAPIView)

urlpatterns = [
    path('hello/', get_hello),
    path('', include(router.urls)),
]
