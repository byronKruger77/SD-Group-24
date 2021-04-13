from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
        path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
        path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
        path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
        path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
        path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
	path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
        path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"), 
	path('Signin/', views.Signinpage, name="Signinpage"),
	path('Login/', views.Loginpage, name="Loginpage") 

]
