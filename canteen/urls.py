"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import ItemList

router = DefaultRouter()
router.register('items', ItemList, basename='polls')

urlpatterns = [
    path('login/', views.LoginwithPassword.as_view(), name="login"),
    path('signup/', views.SignupUser.as_view(), name="signup"),
    path('icategory', views.ItemListView.as_view(), name="icategory"),
    path('cart', views.CartView.as_view(), name="cart"),
    path('payment/', views.PaymentView.as_view(), name="paymnet"),
    path('myorders/', views.OrdersView.as_view(), name="orders"),
    path('orderhistory/', views.OrderHistoryView.as_view(), name="ordershistory"),
]
urlpatterns += router.urls
