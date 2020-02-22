import os
from django.db import models
from django.conf import settings
import datetime
from django.utils import timezone
from django.contrib.auth import settings
import math
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

#from phonenumber_field.modelfields import PhoneNumberField

TAXS_ON_ORDER =8.0

SUBSCRIBE_CHOICES = (
   ('Yes', 'Yes'),
   ('No', 'No')
)

class User(AbstractUser):
    first_name= models.CharField(max_length=30, unique=False)
    last_name= models.CharField(max_length=30, unique=False)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=50, unique=False)
    #phone = models.IntegerField(unique=False)    
    fax= models.CharField(max_length=10, unique=False)
    address1= models.CharField(max_length=30, unique=False)
    address2= models.CharField(max_length=30, unique=False)
    country = models.CharField( max_length=30, unique=False)
    city = models.CharField(max_length=30, unique=False)
    postal_code= models.CharField(max_length=6,unique=False)
    image = models.ImageField()
    seller = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    subscribe=models.CharField(choices=SUBSCRIBE_CHOICES,max_length=10, default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


STATUS_CHOICES = [
     ('v', 'vegitable'),
    ('f', 'fruit'),
    ('e', 'extra'),
]

class Category(models.Model):
    title = models.CharField(max_length=1, choices=STATUS_CHOICES,default='')
    slug = models.SlugField()
    
    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    def __str__(self):
        return self.title

class subcategory(models.Model):
    category = models.ForeignKey('Category',on_delete=models.CASCADE,blank=False, null=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=255, db_index=True, default='')
    price = models.IntegerField(blank=True, null=True)    
    image = models.ImageField()
    # detail_text = RichTextField(max_length=100)
    detail_text = RichTextUploadingField(blank=True)
    category = models.ForeignKey(Category, related_name='productss', on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True)
    published=models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

class Wish(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.item.name

    def get_wish_total(self):
        return self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    price = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_total(self):
        return self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal

class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tax=models.IntegerField(default=0.08)

    def __str__(self):
        return self.user.username

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()
        
        return total

    def get_percentage(self):
        total = 0
        p = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total() 
            p=total*0.08
            floattotal = float("{0:.2f}".format(p))
        return floattotal

    def all_total(self):
        total = 0
        p = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total() 
            p=total*0.08+total
            floattotal = float("{0:.2f}".format(p))
        return floattotal

class BillingAddress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    landmark = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} billing address'

    class Meta:
        verbose_name_plural = "Billing Addresses"

class ContactUs(models.Model):
    name = models.CharField(max_length=30, unique=False)
    email = models.EmailField(unique=True, null=True)
    enquiry = models.CharField(max_length=100)

