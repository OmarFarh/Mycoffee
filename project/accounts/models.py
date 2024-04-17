from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from products.models import Product
# Create your models here.


class Profile (models.Model):

    user = models.OneToOneField(User , on_delete = models.CASCADE)
    product_favorites = models.ManyToManyField(Product)
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    slug = models.SlugField(null = True , blank = True)


    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile , self).save(*args , **kwargs)
        

def creat_profile(sender , **kwargs):
    if kwargs['created']:
        Profile.objects.create(user = kwargs['instance'])

post_save.connect(creat_profile , sender=User)