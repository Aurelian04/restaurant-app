from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order.views import OrderViewSet, OrderItemViewSet

app_name = 'order'

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('order-items', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
]
