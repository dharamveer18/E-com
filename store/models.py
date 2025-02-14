from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,User

# Create your models here.
class User(AbstractUser):
   
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    otp = models.CharField(max_length=6,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class UserImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.user.username
    
    
class Product(models.Model):
    productname = models.CharField(max_length=200)
    price = models.IntegerField(null=True,blank=True)
    description = models.TextField()
    image = models.ImageField(height_field=None, width_field=None, max_length=100, null=None, blank=None, upload_to=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.productname
    
class Images(models.Model):
    name = models.ForeignKey(Product,on_delete=models.CASCADE)
    images = models.ImageField(upload_to=None, null=False, blank=False)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.productname}'
    
class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    
    def __str__(self):
        return self.name
    