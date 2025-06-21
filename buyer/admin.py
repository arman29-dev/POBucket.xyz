from django.contrib import admin

from .models import RouteError
from .models import Buyer, History, Payment


class RouteErrorAdmin(admin.ModelAdmin):
    list_display = ('eid', 'title', 'time')
    search_fields = ('eid', 'field')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'owner', 'seller')
    search_fields = ('product', 'owner', 'date_of_purchase')

class BuyerAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone')
    search_fields = ('id', 'email')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'product', 'status')
    search_fields = ('payment_id', 'order_id', 'product')


admin.site.register(Buyer, BuyerAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(RouteError, RouteErrorAdmin)
admin.site.register(Payment, PaymentAdmin)
