from django.urls import path
from . import views

urlpatterns=[
    path("",views.store,name="alll_store"),
    path("category/<slug:category_slug>/",views.store,name="store"),

]