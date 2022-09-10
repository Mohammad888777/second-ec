from django.db import models
from accounts.models import User
import random

class Code(models.Model):

    number=models.CharField(max_length=200,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    def save(self,*args,**kwargs):

        a=[i for i in range(10)]
        z=[]
        for i in range(5):
            z.append(random.choice(a))
        ss=''.join([str(i) for i in z])
        self.number=ss
        return super().save(*args,**kwargs)

