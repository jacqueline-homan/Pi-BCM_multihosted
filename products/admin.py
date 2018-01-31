from django.contrib import admin
from products.models.product import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	pass