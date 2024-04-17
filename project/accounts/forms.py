from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

class New_Profile(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username' , 'password1' , 'password2' , 'email' , 'first_name' , 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control' , 'id': 'inputUsername'}),
            'email': forms.TextInput(attrs={'class':'form-control' , 'id': 'inputEmail'}),
            'first_name': forms.TextInput(attrs={'class':'form-control' , 'id': 'inputFirstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'id' : 'inputLastName'}),
        }


class Edit_Profile(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['address' , 'city' , 'country']

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control' , 'id': 'city'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'countery'}),
        }

