from django.urls import path
from . import views


urlpatterns = [
    path ('signin/' , views.signin , name= 'Signin'),
    path ('signup/' , views.signup , name= 'Signup'),
    path ('profile/' , views.profile , name= 'Profile'),
    path ('update/' , views.Update_profile , name='Update'),
    path ('logout/' , views.logout_pg , name='Logout'),
    path ('favorits/' , views.show_fvpro , name='Favorits'),
    path ('fvpro/<int:id>/' , views.Produt_favorite , name= 'addfv'),
    path ('deletfv/<int:id>/' , views.remove_fv , name= 'Delet_fv'),
]