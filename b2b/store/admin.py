from django.contrib import admin
from . models import Category,Customer,Product,Order,Profile,SubCategory,Festival,ProductAttribute,City,Business_type
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Festival)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(ProductAttribute)
admin.site.register(City)
admin.site.register(Business_type)



# Mix Profile Info and user Info
class ProfileInline(admin.StackedInline):
    model=Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model=User
    fields=['username','first_name','last_name','email']
    inlines=[ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User,UserAdmin)



class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1  # Add a default empty attribute field



