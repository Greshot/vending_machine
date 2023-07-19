from django.contrib import admin

from apps.vending.models import Product, VendingMachineSlot

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at", "updated_at"]
    ordering = ["-created_at"]

class VendingMachineSlotAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "get_price", "row", "column"]
    ordering = ["row"]

    def get_price(self, obj):
        return obj.product.price
    
    get_price.admin_order_field  = 'product__price'  
    get_price.short_description = 'Product price'

admin.site.register(Product, ProductAdmin)
admin.site.register(VendingMachineSlot, VendingMachineSlotAdmin)
