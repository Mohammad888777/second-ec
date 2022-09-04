from django.shortcuts import render
from store.models import Product



def home(request):

    products=Product.objects.select_related("category").all().filter(is_av=True).order_by("-created")
    contex={
        'products':products
    }
    return render(request,"main/index.html",contex)
