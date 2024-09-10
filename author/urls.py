from django.urls import path
from .import views
app_name = 'author'

urlpatterns =[
    path('login',views.hulogin,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.hulogout,name='logout'),
    path('captcha',views.send_email_captcha,name='email_captcha'),
]