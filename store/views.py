from django.shortcuts import render,get_object_or_404,redirect
from carts.models import CartItem,Cart
from carts.views import _add_cart
from .models import Product
from category.models import Category
from .utils import handle_paginator
from django.db.models import Q



def store(request,category_slug=None,page=None ):

    products=None
    category=None
    res=None

    if category_slug !=None :

        page=request.GET.get("page",1)

        category=get_object_or_404(Category,slug=category_slug)
        products=category.product_set.select_related("category").filter(is_av=True).distinct()

        res=handle_paginator(products,1,page)

    else:

        pages=request.GET.get("page",1)
        products=Product.objects.all().select_related("category")
        res=handle_paginator(products,1,pages)
    
    contex={
        'products':res,
        'category':category
    }
    return render(request,"store/store.html",contex)
    


def product_detail(request,category_slug,product_slug):

    category=get_object_or_404(Category.objects.prefetch_related("product_set"),slug=category_slug)
    product=get_object_or_404(Product.objects.select_related("category"),category=category,slug=product_slug)
    in_cart=CartItem.objects.filter(product=product,cart__cart_id=_add_cart(request)).exists()
    

    contex={
        'product':product,
        'in_cart':in_cart
    }
    return render(request,"store/product_detail.html",contex)



def search(request,page=None):

    q=request.GET.get("q","")
    # res=None
    # products=None
    print(q)
    page=request.GET.get("page",1)

    if page==None or page:
        products=Product.objects.select_related("category").prefetch_related("cartitem_set").filter(
        Q(product_name__icontains=q)|Q(category__category_name__icontains=q)|Q(desc__icontains=q)
        )

    res=handle_paginator(products,1,page)

    contex={
        'q':q,
        'products':res
    }

    return render(request,"store/search.html",contex)

