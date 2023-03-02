from . import views
from django.urls import path

urlpatterns = [
    path('app',views.index,name='index'),
    path('',views.login_req, name='login_req'),
    path('register/',views.register, name='register'),
    path('home',views.home, name='home'),
    # path('myview',views.my_view,name='my_view')




]