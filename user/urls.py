from django.urls import path
from . import views


urlpatterns = [
    path('',views.user_index,name='user-index'),
    path('user-register/',views.user_register,name='user-register'),
    path('user-otp/',views.user_otp,name='user-otp'),
    path('user-login/',views.user_login,name='user-login'),
    path('user-logout/',views.user_logout,name='user-logout'),
    path('user-forgotpassword/',views.user_forgotpassword,name='user-forgotpassword'),
    path('my-profile/',views.my_profile,name='my-profile'),
    path('show-car/',views.show_car,name='show-car'),
    path('book-car/<int:pk>',views.book_car,name='book-car'),
       
]