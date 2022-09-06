from .models import CartItem,Cart
from carts.views import _add_cart



def productsInOrders(request):

    if 'admin' in request.path:
        return {}
    else:
        sum=0
        cart=Cart.objects.get(cart_id=_add_cart(request))
        cartItems=CartItem.objects.filter(cart=cart)
        for item in cartItems:
            sum+=item.quantity
    return {
        'sum':sum
    }