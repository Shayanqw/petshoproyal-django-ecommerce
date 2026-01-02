from django.contrib import admin

from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user','product','variant','size','color','quantity','price']



class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','email', 'city', 'tipax', 'paid','f_name','l_name',"payment_method",'address','create', 'get_price', 'zipcode','code',"user_confirmed_display"]
    # list_editable = ['paid','cash_paid']
    # list_display = ['user','email', 'city', 'tipax', 'paid','f_name','l_name','address','create', 'zipcode','code']
    inlines = [ItemInline]
    def user_confirmed_display(self, obj):
        if obj.payment_method == Order.DELIVERY:
            if obj.user_confirmed:
              return "تایید نهایی"
            return "در انتظار تایید"
        elif obj.payment_method == Order.CART_TO_CART:  # '3'
            if obj.user_confirmed:
                return "اسکرین شات دریافت شده "
            return  "در انتظار اسکرین شات"
        elif obj.payment_method == Order.ONLINE:
            if obj.paid:
                return "پرداخت شده"
            return "در انتظار پرداخت"
        return "N/A"  # Default for other payment methods

    user_confirmed_display.short_description = 'status'

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','start','end','discount','active']
    list_filter = (
        ('code',JDateFieldListFilter),
    )


@admin.register(DeliveryPrice)
class DeliveryPriceAdmin(admin.ModelAdmin):
    list_display = ('from_weight', 'to_weight', 'price')
    list_editable = ('price',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    search_fields = ('name',)


admin.site.register(DeliveryHour)
admin.site.register(Order,OrderAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Province)
admin.site.register(ItemOrder)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(CheckOut)
