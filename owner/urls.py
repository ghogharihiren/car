from . import views
from django.urls import path

urlpatterns = [
    path('',views.login,name='login'),
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'), 
    path('otp/',views.otp,name='otp'),
    path('forgot-password/',views.forgot_password,name='forgot-password'), 
    path('logout/',views.logout,name='logout'),
    path('add-car/',views.add_car,name='add-car'),
    path('view-car/',views.view_car,name='view-car'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('edit-car/<int:pk>',views.edit_car,name='edit-car'),
    path('book-car/',views.book_car,name='book-car'),
    path('complate-journy/<int:pk>',views.complate_journy,name='complate-journy'),
    path('my-bookcar/<int:pk>',views.my_bookcar,name='my-bookcar'),

]