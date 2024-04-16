from django.contrib.auth.models import User
from django.db import models
from product.models import Product


class Order(models.Model):
    ORDERED='ordered'
    SHIPPED='shipped'
    COMPLETED='completed'
    STATUS_CHOICES=(
        (ORDERED, 'Ordered'),
        (SHIPPED,'Shipped'),
        (COMPLETED,'Completed')
    )
        
        
    
    user=models.ForeignKey(User,related_name='orders',blank=True,null=True,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    zipcode=models.CharField(max_length=255)
    place=models.CharField(max_length=255)
    phone=models.CharField(max_length=255) 
    
    created_at=models.DateTimeField(auto_now=True)
    paid= models.BooleanField(default=False)
    paid_amount= models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    
    status= models.CharField(max_length=20,choices=STATUS_CHOICES,default=ORDERED)
    
  
    
    def __str__(self):
          return f"Orden No. {self.id} - {self.first_name} {self.last_name} - Status: {self.status} - {self.paid_amount}"
    
    class Meta:
        ordering = ('-created_at',)
        
    def get_total_price(self):
        if self.paid_amount:
           return self.paid_amount
        return 0
        
class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',blank=True,null=True,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='items',blank=True,null=True,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    quantity= models.IntegerField(default=1)
    
    def get_total_price(self):
        return (  self.price)
         
        
    
    
    
          
    
    
    
    
    
