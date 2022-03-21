from django.urls import path
from . import views


urlpatterns = [
    path('user-index/',views.user_index,name='user-index'),
    path('user-register/',views.user_register,name='user-register'),
    path('user-otp/',views.user_otp,name='user-otp'),
    path('',views.user_login,name='user-login'),
    path('user-logout/',views.user_logout,name='user-logout'),
    path('user-forgotpassword/',views.user_forgotpassword,name='user-forgotpassword'),
    path('my-profile/',views.my_profile,name='my-profile'),
    path('show-car/',views.show_car,name='show-car'),
    path('userview-car/<int:pk>',views.userview_car,name='userview-car'),
    path('add-watchlist/<int:pk>',views.add_watchlist,name='add-watchlist'),
    path('my-watchlist/',views.my_watchlist,name='my-watchlist'),
    path('remove-to-watchlist/<int:pk>',views.remove_to_watchlist,name='remove-to-watchlist'),
    path('book-now/<int:pk>',views.book_now,name='book-now'),
    path('book-now/paymenthandler/<int:pk>', views.paymenthandler, name='paymenthandler'),
    
] 