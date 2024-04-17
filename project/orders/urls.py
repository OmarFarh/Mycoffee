from django.urls import path
from . import views

urlpatterns = [
    path ('add/', views.add_to_cart , name= 'Orders'),
    path ('cart/' , views.cart , name= 'Cart'),
    path ('remove/<int:id>/' , views.remove_prpduct , name='Remove'),
    path ('addpt/<int:id>/' , views.add_qty , name= 'Addqt'),
    path ('less/<int:id>/' , views.less_qty , name= 'Less'),
    path ('payment/' , views.payment , name= 'Payment'),
    path ('myorders/' , views.my_orders , name='My_Orders'),
    path ('ordtl/<int:id>' , views.order_dt , name='Ord_dtl'),
]