from django.shortcuts import render , redirect
from products.models import Product
from .models import OrderDetails , Order , Payment
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='Signin')
def add_to_cart(request):
    
    if 'Pro_id' in request.GET and 'QT' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        
        prodect_id = request.GET['Pro_id']
        qt = request.GET['QT']
        pro = Product.objects.get(id = prodect_id)
        
        order = Order.objects.all().filter(user = request.user , is_finished = False)

        if not Product.objects.filter(id = prodect_id).exists():
            return redirect('Home')

        if order:
            messages.success(request , 'يوجد طلب قديم')
            old_order = Order.objects.get(user = request.user , is_finished = False)
            if OrderDetails.objects.filter(product = pro , order = old_order).exists():
                orderdetails = OrderDetails.objects.get(product = pro , order = old_order)
                orderdetails.quantity = qt
                orderdetails.price = float(pro.price) * float(qt)
                orderdetails.save()
            else:
                price = float(pro.price) * float(qt)
                orderdetails = OrderDetails.objects.create(product = pro , order = old_order , quantity = qt , price = price)
        
        else:
            messages.success(request , 'تم اضافة الطلب')
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            price = float(pro.price) * float(qt)
            orderdetails = OrderDetails.objects.create(product = pro , order = new_order , quantity = qt , price = price)

        return redirect('/products/' + 'product/' + request.GET['Pro_id'])
    else:
        return redirect('Home')
    
@login_required(login_url='Home')
def cart (request):

    if Order.objects.filter(user= request.user , is_finished = False).exists():
        order = Order.objects.get(user= request.user , is_finished = False)
        orderdetails = OrderDetails.objects.filter(order = order)
        total = 0
        count = 0

        for i in orderdetails:

            total += i.price
            count += i.quantity

        context = {
            'order': order,
            'orderdetails': orderdetails,
            'total': total,
            'count' : count,
        }

        return render(request , 'orders/cart.html' , context)
    else:
        return render(request , 'orders/no_order.html')

@login_required(login_url='Signin')
def remove_prpduct(request , id):

    order = OrderDetails.objects.get(id = id)
    if order.order.user.id == request.user.id:
        order.delete()

    return redirect('/orders/' + 'cart/')

@login_required(login_url='Signin')
def add_qty (request , id):

    order_details = OrderDetails.objects.get(id = id)
    if order_details.order.user.id == request.user.id:
        order_details.quantity += 1
        order_details.save()

        order_details.price = order_details.quantity * order_details.product.price
        order_details.save()

    return redirect('/orders/' + 'cart/')


@login_required(login_url='Signin')
def less_qty (request , id):

    order_details = OrderDetails.objects.get(id = id)
    if order_details.order.user.id == request.user.id:
        if order_details.quantity <= 1 :
            order_details.quantity = 1
            order_details.save()
        else:
            order_details.quantity -= 1
            order_details.save()

    order_details.price = order_details.quantity * order_details.product.price
    order_details.save()

    return redirect('/orders/' + 'cart/')

@login_required(login_url='Signin')
def payment (request):

        
    if Order.objects.filter(user= request.user , is_finished = False).exists():
        order = Order.objects.get(user= request.user , is_finished = False)
        orderdetails = OrderDetails.objects.filter(order = order)

        if 'address' in request.POST and 'phone' in request.POST and 'cardnumber' in request.POST and 'expire' in request.POST and 'cvv' in request.POST and 'submet' in request.POST and request.method == 'POST':

            address = request.POST['address']
            phone = request.POST['phone']
            card_number = request.POST['cardnumber']
            expire = request.POST['expire']
            cvv = request.POST['cvv']

            pAyment = Payment( order = order , address = address , phone = phone , card_number = card_number , expire =  expire, cvv = cvv)
            pAyment.save()

            order.is_finished = True
            order.save()
            return render(request , 'orders/no_order.html')
        
        total = 0
        count = 0

        for i in orderdetails:

            total += i.price
            count += i.quantity

        context = {
            'order': order,
            'orderdetails': orderdetails,
            'total': total,
            'count' : count,
        }

        return render(request , 'orders/confirm_oder.html' , context)
    
    else:
        return render(request , 'orders/no_order.html')

@login_required(login_url='Signin')
def my_orders(request):

    orders = Order.objects.filter(user = request.user)
    if orders.exists():

        context = {
            'Orders': orders,
        }

        return render(request , 'orders/orders.html' , context)
    
    else:
        return render(request , 'orders/no_order.html')
    
@login_required(login_url='Signin')
def order_dt(request , id):

    order = Order.objects.get(id = id)

    if order.user == request.user:

        products = OrderDetails.objects.filter(order = order)
        payment  = Payment.objects.get(order = order)

        context = {
            'productes': products,
            'dtl': payment
        }

        return render(request , 'orders/orderdtl.html' , context)
    
    else:
        return render(request , 'orders/no_order.html')
    