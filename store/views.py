from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from category.models import Category

def store(request,category_slug=None):

    products=None
    category=None
    if category_slug !=None:
        category=get_object_or_404(Category,slug=category_slug)
        products=category.product_set.select_related("category").filter(is_av=True).distinct()
    else:
        products=Product.objects.all().select_related("category")
    
    contex={
        'products':products,
        'category':category
    }
    return render(request,"store/store.html",contex)
    
