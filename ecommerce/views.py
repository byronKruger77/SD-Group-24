from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import datetime        
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from .models import *
from cart.cart import Cart

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        u = request.user
        customer = Customer.objects.get(user_id=u.id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}

    return render(request, 'ecommerce/Store.html', context)

# Cart functionalities

def cart_add(request, id):
    
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.add(product=product)
    else:
        print("User must be logged in!")

    return HttpResponse(status=204)

def item_clear(request, id):
    
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Product.object.get(id=id)
        cat.remove(product)
        return redirect("cart_detail")
    else:
        print("User must be logged in!")
        return HttpResponse(status=204)


def item_increment(request, id):

    if request.user.is_authenticated:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.add(product=product)
        return redirect("cart_detail")
    else:
        print("User must be logged in")
        return HttpResponse(status=204)

def item_decrement(request, id):

    if request.user.is_authenticated:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.decrement(product=product)
        return redirect("cart_detail")
    else:
        print("USer must be logged in")
        return HttpResponse(status=204)

def cart_clear(request):
    
    if request.user.is_authenticated:
        cart = Cart(request)
        cart.clear()
        return redirect("cart_detail")
    else:
        print("User must be logged in")
        return HttpResponse(status=204)


def cart_detail(request):
    
    if request.user.is_authenticated:
        cart = Cart(request)
        total = sum([float(value['price']) for key,value in cart.cart.items()])
        context = {'total':total}
        return render(request, 'ecommerce/Cart.html', context)
    else:
        return HttpResponse(status=204)

"""def cart(request):

    if request.user.is_authenticated:
        u = request.user
        customer = Customer.objects.get(user_id=u.id)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, 'ecommerce/Cart.html', context)"""



@csrf_exempt
def checkout(request):

    if request.user.is_authenticated:
        u = request.user
        customer = Customer.objects.get(user_id=u.id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        cart = Cart(request)
        total = sum([float(value['price']) for key,value in cart.cart.items()])

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'total':total}

    return render(request, 'ecommerce/Checkout.html', context)



def updateItem(request):

    data=json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    u = request.user
    customer = Customer.objects.get(user_id=u.id)

    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item updated', safe=False)


@csrf_exempt
def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        u = request.user
        customer = Customer.objects.get(user_id=u.id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                    )

    else:
        print('user is not logged in...')

    return JsonResponse('Payment Complete', safe=False)

def Signinpage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()


	context = {'form' : form}
	return render(request, 'ecommerce/signin.html', context)
