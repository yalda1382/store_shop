from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
import datetime


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    shipping_full_name= models.CharField(max_length=100)
    shipping_email= models.CharField(max_length=300)
    shipping_phone=models.CharField(max_length=20, blank=True)
    shipping_address1=models.CharField(max_length=255, blank=True)
    shipping_address2=models.CharField(max_length=255, blank=True)
    shipping_city=models.CharField(max_length=50, blank=True)
    shipping_state=models.CharField(max_length=50, blank=True)
    shipping_zipcode=models.CharField(max_length=20, blank=True)
    shipping_country=models.CharField(max_length=50, default='IRAN')
    shipping_old_cart=models.CharField(max_length=200,blank=True,null=True)
    
    class Meta:
        verbose_name_plural = "Shipping Addresses"
        
    def __str__(self):
        return f"Shipping Address from {self.full_name}"


    
class Order(models.Model):
    STATUS_ORDER=[
        ('pending','paymant'),
        ('processing','process'),
        ('shipped','sending items to  post'),
        ('deleverd','deliverd')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email=models.CharField(max_length=300)
    shipping_address = models.TextField(max_length=150000)
    amount_paid=models.DecimalField(max_digits=12, decimal_places=0, default=0)
    date_ordered=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_ORDER,default='pending')
    last_update=models.DateTimeField(auto_now=True)
    def save(self,*args, **kwargs):
        if self.pk:
            old_status=Order.objects.get(id=self.pk).status
            if old_status != self.status:
                self.last_update=datetime.datetime.now()
        super().save(*args, **kwargs)

    
    class Meta:
        verbose_name_plural = "Orders"
        
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
 
 
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1 )
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    
    class Meta:
        verbose_name_plural = "Order Items"
        
    def __str__(self):
        return f"{self.quantity} of {self.product} in Order {self.order.id}"