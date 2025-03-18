from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import  post_save
from django.utils.timezone import now
# Models (Database)


class Business_type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name









class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified=models.DateTimeField(User,auto_now=True)
    phone=models.CharField(max_length=20,blank=True)
    address1=models.CharField(max_length=200,blank=True)
    address2=models.CharField(max_length=200,blank=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)
    state=models.CharField(max_length=200,blank=True)
    zipcode=models.CharField(max_length=200,blank=True)
    country=models.CharField(max_length=200,blank=True)
    is_seller=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    GST_number=models.CharField(max_length=15,default='',blank=True,null=True)
    work_days=models.CharField(max_length=500,default='',blank=True,null=True)
    business_type = models.ManyToManyField(Business_type, blank=True)  # Changed to ManyToManyField
    establishment = models.DateField(blank=True, null=True)
    employee_count=models.IntegerField(default=1)
    company_details=models.CharField(max_length=2500,blank=True)
    want_to_prime=models.BooleanField(default=False)
    seller_req_choice = [
        ('pending', 'Pending'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    ]
    seller_req = models.CharField(
        max_length=10,
        choices=seller_req_choice,
        blank=True,  # Allow the field to be left blank
        null=True,  # Allow null values in the database
        default='pending',
    )
    def __str__(self):
        return self.user.username

# Create a user profile by default when user signs up
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()

# Automate the Profile thing
post_save.connect(create_profile,sender=User)


class Festival(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    banner_image = models.ImageField(upload_to='upload/festival/')

    def __str__(self):
        return self.name

    def remaining_time(self):
        from datetime import date
        if self.end_date:
            return (self.end_date - date.today()).days
        return 0


class Category(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, blank=True, null=True)  # Make sure this field has data
    image = models.ImageField(upload_to='upload/category_images', blank=True, null=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload/subcategory_images', blank=True, null=True)
    

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"





class Product(models.Model):
    SEASON_CHOICES = [
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('rainy', 'Rainy'),
    ]
    name=models.CharField(max_length=100)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=9)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    description=models.CharField(max_length=250,default='',blank=True,null=True)
    image=models.ImageField(upload_to='upload/product/')

    image_1 = models.ImageField(upload_to='upload/product/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='upload/product/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='upload/product/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='upload/product/', null=True, blank=True)
    festival = models.ForeignKey(Festival, on_delete=models.SET_NULL, null=True, blank=True)
    # attributes = models.ManyToManyField(AtPd)  # or ForeignKey if one-to-many
    keywords = models.CharField(
        max_length=255,  # You can adjust the length based on your requirements
        blank=True,      # It's okay if no keywords are added
        null=True,       # Keywords can be empty initially
        help_text="Comma-separated list of keywords (e.g., 'organic milk, whole milk, dairy milk')"
    )

    season = models.CharField(
        max_length=10,
        choices=SEASON_CHOICES,
        blank=True,  # Allow the field to be left blank
        null=True,   # Allow null values in the database
        default='none',
    )
    

    # Connect user, reffer product is belong to User
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='products')

    # Add Sale Tag Stuff
    on_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,decimal_places=2,max_digits=10)
    created_at = models.DateTimeField(default=now, editable=False)

   
    def __str__(self):
        return self.name



class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.ImageField(default=1)
    address=models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=50,default='',blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product}"



class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_name}: {self.attribute_value}"


class Enquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Enquiry from {self.name}"
    

class BestPriceRequest(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='best_price_requests')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.name} for {self.product.name}"
    

import random
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

User = get_user_model()

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)

    @staticmethod
    def generate_otp():
        return f"{random.randint(100000, 999999)}"



class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='upload/images/')

    def __str__(self):
        return self.name
