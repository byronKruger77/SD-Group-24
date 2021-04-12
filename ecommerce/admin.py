from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# Define an inline admin descriptor for Customer model
"""class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    versbose_name_plural = 'customer'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inline = (CustomerInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)"""
