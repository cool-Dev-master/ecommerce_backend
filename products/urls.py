from django.urls import path
# from django.utils.functional import lazy
from .views import ProductsView, Home, ProductsCreateUpdate

# get_home_lazy = lazy(lambda: Home(), list)
urlpatterns = [
    # path('', get_home_lazy, name='home'),
    path('', Home, name='home'),
    path('get/', ProductsView, name='list_products'),
    path('get/<int:pk>', ProductsView, name='get_products'),
    path('create/', ProductsCreateUpdate, name='products_create_update'),
    # path('products/', ProductsView, name='get_products')
]