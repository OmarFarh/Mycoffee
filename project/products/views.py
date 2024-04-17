from django.shortcuts import render , get_object_or_404
from .models import Product
# Create your views here.


def products(request):

    PRO = Product.objects.all()

    if request.method == 'GET' and 'Search' in request.GET:
        PRO = Product.objects.filter(name__icontains = request.GET['Search'])
        if not PRO:
            PRO = Product.objects.filter(description__icontains = request.GET['Search'])

    if request.method == 'GET' and 'Pro_Name' in request.GET:

        PRO = Product.objects.filter(name__icontains = request.GET['Pro_Name'] , description__icontains = request.GET['Pro_Dsc'])

        if len(request.GET['Price_Min']) >= 1 and len(request.GET['Price_Max']) >= 1:

            Min = int(request.GET['Price_Min'])
            Max = int(request.GET['Price_Max'])

            PRO = Product.objects.filter(name__icontains = request.GET['Pro_Name'] , description__icontains = request.GET['Pro_Dsc'] , price__range = (Min , Max))

    context = {
        'products': PRO
    }

    return render(request , 'Products/products.html' , context)

def product(request , id):

    context = {
        # 'product' : Product.objects.get(id = id)
        'product' : get_object_or_404(Product , id = id)
    }

    return render(request , 'Products/product.html' , context)


def search(request):

    return render(request , 'Products/search.html')