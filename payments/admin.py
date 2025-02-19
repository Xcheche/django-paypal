from django.contrib import admin
from.models import Product, Category
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category', 'status', 'availability']
    list_filter = ['status', 'availability', 'category']
    search_fields = ['name', 'description']
    # prepopulated_fields = {'slug': ('name',)}
 
 
 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    # prepopulated_fields = {'slug': ('name',)}   
    
admin.site.register(Category, CategoryAdmin)    
admin.site.register(Product, ProductAdmin)   