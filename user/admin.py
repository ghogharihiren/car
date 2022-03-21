from django.contrib import admin
from user.models import *


@admin.register(passenger)
class adminuser(admin.ModelAdmin):
    list_display = ['name', 'email',]
    
@admin.register(cart)
class cartAdmin(admin.ModelAdmin):
    list_display = ['uid']    
