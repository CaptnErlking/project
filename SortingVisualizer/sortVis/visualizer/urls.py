from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate-array/', views.generate_array, name='generate_array'),
    path('sort-array/', views.sort_array, name='sort_array'),
]
