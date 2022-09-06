from re import I
from django.shortcuts import render,get_object_or_404,redirect
from .models import Cart,CartItem
from store.models import Product,Variation
from django.http import HttpResponse


def _add_cart(request):

    cart_session=request.session.session_key
    if not cart_session:
        cart_session=request.session.create()
    return cart_session



def add_cart(request,product_pk):

    product=get_object_or_404(Product,pk=product_pk)
    product_variation=[]
    if request.method=="POST":
       for item in request.POST:
        key=item
        value=request.POST[key]
        try:
            var=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
            product_variation.append(var)
            # print(var.variation_category)
        except:
            pass

    try:
        cart=Cart.objects.get(cart_id=_add_cart(request))

    except Cart.DoesNotExist:

        cart=Cart.objects.create(
            cart_id=_add_cart(request)
        )

    is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if product_variation in ex_var_list:
            # increase the cart item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart=cart,        
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')





def cart(request):

    total=0
    quantity=0
    tax=0
    grand_total=0
    cart=Cart.objects.prefetch_related("cartitem_set").get(cart_id=_add_cart(request))
    cartItems=CartItem.objects.filter(cart=cart)

    for cartItem in cartItems:

        total+=(cartItem.product.price*cartItem.quantity)
        quantity+=cartItem.quantity

    tax=(total*2)/100
    grand_total=tax+total

    contex={
        'cartItems':cartItems,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total
    }

    return render(request,"carts/cart.html",contex)




def remove_cart(request,product_pk,cartItem_id):

    cart=Cart.objects.get(cart_id=_add_cart(request))
    product=get_object_or_404(Product,pk=product_pk)
    cartItem=get_object_or_404(CartItem,product=product,cart=cart,pk=cartItem_id)
    if cartItem.quantity>1:
        cartItem.quantity-=1
        cartItem.save()
    else:
        cartItem.delete()
    return redirect("cart")




def delete_cartitem(request,product_pk,cartItem_id):

    cart=Cart.objects.get(cart_id=_add_cart(request))
    product=get_object_or_404(Product,pk=product_pk)
    cartItem=get_object_or_404(CartItem,product=product,cart=cart,pk=cartItem_id)
    cartItem.delete()
    return redirect(request.META.get("HTTP_REFERER"))