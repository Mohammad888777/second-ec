from django.db import models

from django.db import models
from store.models import Product
from store.models import Variation


class Cart(models.Model):

    cart_id=models.CharField(max_length=200,blank=True)

    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,)
    variations=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)


    def __str__(self) -> str:
        return str(self.product)

    def total_sum(self):
        
        return self.product.price * self.quantity