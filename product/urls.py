from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductAPIView, CategoryAPIView, get_hello, ProductTemplateList

router = DefaultRouter()
router.register('category', CategoryAPIView)
router.register('', ProductAPIView)

urlpatterns = [
    path('hello/', get_hello),
    path('list/', ProductTemplateList.as_view()),
    path('', include(router.urls)),
]
