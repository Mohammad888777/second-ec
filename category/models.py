from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class Category(models.Model):

    category_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    desc=models.CharField(max_length=200,blank=True,)
    cat_image=models.ImageField(upload_to="CateGoryImage",null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=["png","jpg","jpeg"])])

    def __str__(self):

        return self.category_name

    class Meta:
        verbose_name="category"
        verbose_name_plural="category"