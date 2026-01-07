from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from  django.contrib.auth.models import User
from django.db.models.signals import post_save

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    
class Customer(models.Model):
   first_name=models.CharField(max_length=200)
   last_name=models.CharField(max_length=200)
   email=models.EmailField(unique=True)
   phone=models.CharField(max_length=20,unique=True)
   password=models.CharField(max_length=200)
   def __str__(self):
         return f"{self.first_name} {self.last_name}"  
     
     
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    phone=models.CharField(max_length=20, blank=True)
    address1=models.CharField(max_length=255, blank=True)
    address2=models.CharField(max_length=255, blank=True)
    city=models.CharField(max_length=50, blank=True)
    state=models.CharField(max_length=50, blank=True)
    zipcode=models.CharField(max_length=20, blank=True)
    country=models.CharField(max_length=50, default='IRAN')
    old_cart=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return f"{self.user.username} Profile"
    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()
post_save.connect(create_user_profile, sender=User)


class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True,default="")
    price=models.DecimalField(max_digits=12,decimal_places=0,default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    star=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    picture=models.ImageField(upload_to='products/',null=True,blank=True)
    Is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(max_digits=12,decimal_places=0,default=0)
    def __str__(self):
        return self.name
    

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE
        )
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=200,default="",blank=False)
    phone=models.CharField(max_length=20,default="",blank=False)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.product
    
