from django.urls import path
from . import views
from store.views import store

urlpatterns=[
    path("",views.cart,name="cart"),

    path("add_cart/<str:product_pk>/",views.add_cart,name="add_cart"),
    path("remove_cartitem/<str:product_pk>/<str:cartItem_id>/",views.remove_cart,name="remove_cartitem"),
    path("delete_cartItem/<str:product_pk>/<str:cartItem_id>/",views.delete_cartitem,name="delete_cartItem"),
]