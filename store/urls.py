from django.urls import path
from . import views

urlpatterns=[

    path("aa/",views.store,name="all_store"),



    path("aa/<str:page>/",views.store,name="all_store"),

   path("category/<slug:category_slug>/",views.store,name="store"),
    path("category/<slug:category_slug>/<str:page>/",views.store,name="store"),
    

    path("category/<slug:category_slug>/<slug:product_slug>/detail",views.product_detail,name="product_detail"),
  




    path("search",views.search,name="search"),
    path("search/<str:page>/",views.search,name="search"),

]