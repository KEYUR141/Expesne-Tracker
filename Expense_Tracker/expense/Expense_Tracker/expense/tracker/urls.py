from django.urls import path
from tracker.views import *

urlpatterns = [
    path('login/',login_page,name="login_page"),
    path('logout/',logout_page,name="logout_page"),
    path('home/',index,name='index'),
    path('delete-transaction/<uuid>',deleteTransaction,name='deleteTransaction'),
    path('register/',register_page,name="register_page"),
]
