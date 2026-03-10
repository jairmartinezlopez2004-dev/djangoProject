


from django.contrib import admin
from users.models import Product




# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count', 'description')
    list_filter = ('name', 'price', 'count', 'description')
    search_fields = ('name',)

