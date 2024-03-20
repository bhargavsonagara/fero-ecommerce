from django.contrib import admin
from django.urls import path, include

from drfapi.views import CustomerListCreateAPIView, CustomerUpdateAPIView, ProductListCreateAPIView, \
    OrderListCreateAPIView

urlpatterns = [
    path('customers/', include([
        path('', CustomerListCreateAPIView.as_view(), name='customer-listcreate'),
        path('<int:pk>/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    ])),

    path('products/', include([
        path('', ProductListCreateAPIView.as_view(), name='product-listcreate'),
    ])),

    path('orders/', include([
        path('', OrderListCreateAPIView.as_view(), name='order-listcreate'),
    ]))
]
