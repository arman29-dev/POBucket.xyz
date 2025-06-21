from django.contrib import admin

from .models import Product, Bid, Sale
from .models import RouteError
from .models import Seller


class RouteErrorAdmin(admin.ModelAdmin):
    list_display = ('eid', 'title', 'time')
    search_fields = ('eid', 'field')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pid', 'name', 'publish_date', 'bid_status', 'seller')
    search_fields = ('pid', 'name', 'seller')

class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'fullname', 'phone')
    search_fields = ('username', 'email')

class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'sale_date', 'final_price', 'buyer')
    search_fields = ('product', 'sale_date', 'seller')

class BidAdmin(admin.ModelAdmin):
    list_display = ('product', 'bidder', 'bid_amount', 'bid_time')
    search_fields = ('product', 'bidder')


admin.site.register(RouteError, RouteErrorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Bid, BidAdmin)
