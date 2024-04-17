from django.urls import path
from . import views

urlpatterns = [
    path('' , views.products , name= 'Products'),
    path('product/<int:id>' , views.product , name= 'Product'),
    path('search/' , views.search , name= 'Search'),
]
