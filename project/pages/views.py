from django.shortcuts import render
from products.models import Product
# Create your views here.


def index(request):

    context = {
        'products': Product.objects.all().order_by('-publish_date')
    }

    return render(request , 'pages/index.html' , context)

def about(request):

    return render(request , 'pages/about.html')

def cofee(request):

    return render(request , 'pages/coffee.html')