from django.db import models
from django.core.validators import FileExtensionValidator
from category.models import Category
 
class Product(models.Model):

    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    desc=models.TextField(max_length=200,blank=True,null=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to="ProfuctImg",null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])
    stock=models.IntegerField()
    is_av=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    is_av.bool=True

    def __str__(self) -> str:
        return str(self.product_name)
