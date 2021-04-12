from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
import datetime        

from .models import *
# Create your views here.




def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']
	products = Product .objects.all()
	context = {'products':products, 'cartItems':cartItems}

	return render(request, 'ecommerce/Store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'ecommerce/Cart.html', context)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout(request):
	context = {}

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	
	return render(request, 'ecommerce/Checkout.html', context)



def updateItem(request):

	data=json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)


	customer = request.user.customer
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

	return JsonResponse('Item was added', safe=False)
 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
	
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
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

def Loginpage(request):
	if request.user.is_authenticated:
		return redirect('store')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'ecommerce/login.html', context)

