from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from .forms import *
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from products.models import Product
# Create your views here.


def signin(request):

    if request.method == 'POST':
        data = authenticate(request , username = request.POST['user'] , password = request.POST['password'])
        if data is not None:
            if 'remember' not in request.POST:
                request.session.set_expiry(0)
            login(request , data)
            return redirect('Home')
        else :
           messages.error(request , 'اسم المستخدم او كلمة المرور غير صحيحة')  

    return render(request , 'account/signin.html')


def signup(request):

    context = {
        'signup': New_Profile,
        'add_info': Edit_Profile,
    }

    if request.method == 'POST':

        if User.objects.filter(email = request.POST['email']).exists():
            messages.error(request , 'Email is oredy exist')
        else:
            data_signup = New_Profile(request.POST)
            if data_signup.is_valid():
                data_signup.save()
                us = User.objects.get(username = data_signup.cleaned_data['username'])
                pro = Profile.objects.get(user = us)
                add_info = Edit_Profile( request.POST , instance=pro)
                add_info.save()
                return redirect('Signin')

    return render(request , 'account/signup.html' , context)

@login_required(login_url='Signin')
def profile(request):

    return render(request , 'account/profile.html')

@login_required(login_url='Signin')
def Update_profile (request):

    Pro = Profile.objects.get(user = request.user)

    profile = Edit_Profile(instance= Pro)

    if request.method == 'POST' and 'address' in request.POST:
        profile = Edit_Profile( request.POST , instance= Pro)
        if profile.is_valid():
            request.user.first_name = request.POST['firstname']
            request.user.last_name = request.POST['lastname']
            request.user.save()
            profile.save()
            return redirect('Profile')

    context = {
        'profile': profile,
    }

    return render(request , 'account/update_info.html' , context)


def logout_pg (request):

    if request.user.is_authenticated:
        logout(request)
        return redirect('Home')
    

def Produt_favorite (request , id):

    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(id = id)
        if Profile.objects.filter(user = request.user , product_favorites = pro_fav).exists():
            messages.success(request , 'Alredy product in vavorite list')
        else:
            usre_profile = Profile.objects.get(user = request.user)
            usre_profile.product_favorites.add(pro_fav)
            messages.success(request , 'Product in vavorite list now')
    else:
        messages.error(request , 'You must will be login')
        
    return redirect('/products/'+ 'product/' + str(id))


def show_fvpro (request):

    usre_profile = Profile.objects.get(user = request.user)

    context = {
        'products': usre_profile.product_favorites.all(),
    }

    return render(request , 'products/Fvproducts.html' , context)


def remove_fv (request , id):

    Fv = Profile.objects.get(user = request.user)
    if Fv.user == request.user:
        pro = Product.objects.get(id= id)
        Fv.product_favorites.remove(pro)
    return redirect('Favorits')

