
from django.contrib import admin
from owner.models import *



# Register your models here.
#admin.site.register(owner)

@admin.register(owner)
class Adminowner(admin.ModelAdmin):
    list_display = ['name','email','mobile','verify']
    
@admin.register(car)
class Admincar(admin.ModelAdmin):
    list_display = ['name','model']   

# Register your models here.
@admin.register(startpoint)
class Adminstartpoint(admin.ModelAdmin):
    list_display=['name']
    
@admin.register(destination)
class Admindestination(admin.ModelAdmin):
    list_display=['name']    