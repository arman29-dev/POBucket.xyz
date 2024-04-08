from django.contrib import admin

from .models import RouteError
from .models import Buyer, History


class RouteErrorAdmin(admin.ModelAdmin):
    list_display = ('title', 'field', 'time')
    search_fields = ('title', 'field')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'owner', 'seller_phone_no')
    search_fields = ('product_name', 'owner', 'date_of_purchase')

class BuyerAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'phone')
    search_fields = ('id', 'email')


admin.site.register(Buyer, BuyerAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(RouteError, RouteErrorAdmin)