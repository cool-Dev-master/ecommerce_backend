from django.urls import path
# from django.utils.functional import lazy
from .views import ProductsView, Home, ProductsCreate, ProductsUpdate, CategoryView, CategoryCreate, CategoryUpdate

# get_home_lazy = lazy(lambda: Home(), list)
urlpatterns = [
    # path('', get_home_lazy, name='home'),
    path('', Home, name='home'),
    path('get/', ProductsView, name='list_products'),
    path('get/<int:pk>', ProductsView, name='get_products'),
    path('create/', ProductsCreate, name='products_create'),
    path('update/<int:pk>', ProductsUpdate, name='products_update'),

    path('category/get/', CategoryView, name='list_category'),
    path('category/get/<str:pk>', CategoryView, name='get_category'),
    path('category/create', CategoryCreate, name='category_create'),
    path('category/update/<int:pk>', CategoryUpdate, name='category_update'),
]