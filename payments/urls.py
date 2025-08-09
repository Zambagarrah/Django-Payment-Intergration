from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path("mpesa/", views.mpesa_checkout, name="mpesa_checkout"),
]
