from django.contrib import admin

from .models import Product, Bid, Sales
from .models import RouteError
from .models import Seller


class RouteErrorAdmin(admin.ModelAdmin):
    list_display = ('title', 'field', 'time')
    search_fields = ('title', 'field')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'publish_date', 'bid_status', 'seller')
    search_fields = ('pid', 'name', 'seller')

class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fullname', 'phone')
    search_fields = ('username', 'email')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('product', 'date_of_sale', 'sale_price', 'seller')
    search_fields = ('product', 'date_of_sale', 'seller')

class BidAdmin(admin.ModelAdmin):
    list_display = ('product', 'bidder', 'bid_amount', 'bid_time')
    search_fields = ('product', 'bidder')


admin.site.register(RouteError, RouteErrorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(Bid, BidAdmin)