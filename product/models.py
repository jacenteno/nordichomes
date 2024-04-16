from django.db import models



from PIL import Image
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User


class Category(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField()
    
    class Meta: 
        verbose_name_plural ="Catergories"
        
        ordering = ('name',)
        
        
    def __str__(self):
         return self.name

class Product(models.Model):
    category= models.ForeignKey(Category,related_name= 'products',on_delete=models.CASCADE)
    name = models.name = models.CharField(max_length=255,blank=False, null=False)   
    slug=models.SlugField()
    description=models.TextField(blank=True, null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)  
    image=models.ImageField(upload_to='uploads/',blank=True,null=True)  #importante.
    thumbnail=models.ImageField(upload_to='uploads/',blank=True,null=True)  #importante.
   
    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
         return self.name
     
    def display_price(self):
        return self.price / 100
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail=self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img = img.convert('RGB')  # Convert image to RGB mode
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    
class Review(models.Model):
    product = models.ForeignKey(Product,related_name='reviews',on_delete=models.CASCADE)
    rating= models.IntegerField(default=3)
    content = models.TextField()
    created_by= models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
   