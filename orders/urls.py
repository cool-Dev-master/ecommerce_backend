from django.urls import path
from .views import OrdersView, OrdersCreate

urlpatterns = [
    path('get/', OrdersView, name="get_orders"),
    path('get/<str:pk>', OrdersView, name="get_orders_list"),
    path('create/', OrdersCreate, name='orders_create_update'),
]