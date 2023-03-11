from django.urls import path
from ethapp import views as ethapp_views

urlpatterns=[
    path('', ethapp_views.index, name="home"),
    path('eth_test/', ethapp_views.eth_test, name="eth_test"),
    path('eth_hello/', ethapp_views.eth_hello, name="eth_hello")
]