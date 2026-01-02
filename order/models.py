from django.db import models
from django.contrib.auth.models import User
from home.models import *
from django.forms import ModelForm
from django_jalali.db import models as jmodels

from utils.defines import get_delivery_price



class Province(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    province = models.ForeignKey(Province,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    ONLINE='1'
    DELIVERY='2'
    CART_TO_CART='3'

    payment_method_arr = (
        (ONLINE, 'درگاه انلاین'),
        (DELIVERY, 'درب منزل'),
        (CART_TO_CART, 'کارت به کارت'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    create = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(blank=True,null=True)
    phone = models.PositiveIntegerField(blank=True,null=True)
    delivery_hour = models.ForeignKey('order.DeliveryHour', models.SET_NULL, 'oo_delivery_hour', null=True)
    paid = models.BooleanField(default=False)
    tipax = models.BooleanField(default=False)
    code = models.CharField(max_length=200,null=True)
    email = models.EmailField(blank=True,null=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=10,blank=True,null=True)
    province = models.ForeignKey(Province,on_delete=models.CASCADE,null=True,blank=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,null=True,blank=True)
    payment_method=models.CharField(max_length=1,choices=payment_method_arr,default='1')
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True) # only payment method is cart to card
    tracking_code = models.CharField(max_length=20, blank=True, null=True)
    user_confirmed= models.BooleanField(default=True)

    def __str__(self):
        if self.user:
            return self.user.username
        return f"{self.id}"

    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.city and self.city.name == 'تهران':
            if self.discount:
                discunt_price = (self.discount / 100) * total
                return int(total - discunt_price)
        elif not self.tipax:
            items = self.order_item.all()
            weight = 0
            for i in items:
                variant = i.variant
                if variant:
                    weight += i.variant.weight * i.quantity
            total += get_delivery_price(weight)
            if self.discount:
                discunt_price = (self.discount / 100) * total
                return int(total - discunt_price)
        else:
            if self.discount:
                discunt_price = (self.discount / 100) * total
                return int(total - discunt_price)

        return total


class ItemOrder(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username

    def size(self):
        return self.variant.size_variant.name

    def color(self):
        return self.variant.color_variant.name

    def price(self):
        if self.product.status != 'None':
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email','f_name','l_name','address','zipcode','phone','province','city']


class CheckOut(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    creditNumberCard = models.CharField(default=0,null=True,blank=True, max_length=255)
    date = models.CharField(max_length=300,null=True,blank=True)
    trackingCode = models.CharField(max_length=30,null=True,blank=True)
    trans_id = models.CharField(max_length=255,null=True,blank=True)
    invoice_id = models.CharField(max_length=255, null=True, blank=True)
    bank = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    finalPrice = models.PositiveIntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.order.user.username

    def final_price(self):
        return self.order.get_price()


class Coupon(models.Model):
    code = models.CharField(max_length=100,unique=True)
    active = models.BooleanField(default=False)
    start = jmodels.jDateTimeField()
    end = jmodels.jDateTimeField()
    discount = models.IntegerField()


"""
Delivery models
Mostafa Rasouli
mostafarasooli54@gmail.com
2023-12-15
"""


class DeliveryPrice(models.Model):
    from_weight = models.PositiveIntegerField()
    to_weight = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.from_weight} - {self.to_weight}'


class DeliveryHour(models.Model):
    from_hour = models.CharField(max_length=30)
    to_hour = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.from_hour} - {self.to_hour}'