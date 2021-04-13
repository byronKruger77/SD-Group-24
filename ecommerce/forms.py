from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    cellphone_no = forms.CharField()

	class Meta:
		model = User
		fields = ('first_name','last_name', 'username', 'email', 'cellphone_no', 'password1' ,'password2')
