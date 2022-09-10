from django.db.models.signals import post_save
from accounts.models import User
from .models import Code



def autoMake(sender,instance,created,**kwargs):
    if created:
        Code.objects.create(
            user=instance
        )
post_save.connect(autoMake,sender=User)
