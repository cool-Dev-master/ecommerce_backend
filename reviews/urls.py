from django.urls import path
from .views import ReviewCreate, ReviewView, ReviewDelete, ReviewUpdate

urlpatterns = [
    path('get/', ReviewView, name='list_reviews'),
    path('get/<int:pk>', ReviewView, name='get_reviews'),
    path('create/', ReviewCreate, name='review_create'),
    path('update/<int:pk>', ReviewUpdate, name='reviews_update'),
    path('delete/<int:pk>', ReviewDelete, name='review_delete'),
]