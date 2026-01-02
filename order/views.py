import traceback
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from .models import *
from cart.models import *
from .forms import CouponForm,CheckOutForm,CartForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
# from suds import client
import requests
import json
import jdatetime
from django.utils.crypto import get_random_string
import ghasedak
from django.views import View
import uuid
from utils import pg_api
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from log.defines import save_log
from django.contrib.auth.decorators import login_required
from .signals import disable_signals
from django.db.models.signals import pre_save
# Create your views here.

#
# def order_details(request,order_id):
#     order = Order.objects.get(id=order_id)
#     form = CouponForm()
#     if request.method == 'POST':
#         checkOutForm = CheckOutForm(request.POST)
#         if checkOutForm.is_valid():
#             data = checkOutForm.cleaned_data
#             checkOut = CheckOut.objects.create(order=order,creditNumberCard=data['creditNumberCard'],date=data['date'],trackingCode=data['trackingCode'],finalPrice=order.get_price())
#             order.paid = True
#             for item in ItemOrder.objects.filter(order_id=order_id):
#                 if item.product.status == 'None':
#                     product = Product.objects.get(id=item.product.id)
#                     product.amount -= item.quantity
#                     product.sell += item.quantity
#                     product.save()
#                 else:
#                     variant = Variants.objects.get(id=item.variant.id)
#                     variant.amount -= item.quantity
#                     variant.save()
#             order.save()
#             checkOut.save()
#             messages.success(request, 'اطلاعات با موفقیت ثبت شد ، حداکثر تا 4 ساعت آتی با شما تماس گرفته خواهد شد .', 'success')
#             return redirect('home:home')
#     else:
#         checkOutForm = CheckOutForm()
#     context = {'order':order,'form':form,'checkOutForm':checkOutForm}
#     return render(request,'order/order.html',context)

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        email = request.POST.get('email')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')
        province = request.POST.get('province')
        city = request.POST.get('city')
        code = get_random_string(length=8)


        order = Order.objects.create(user_id=request.user.id, email=email,
                                     f_name=f_name, l_name=l_name, address=address,
                                     zipcode=zipcode, code=code, phone=phone, province_id=province, city_id=city)

        cart = Cart.objects.filter(user_id=request.user.id)
        for c in cart:
            ItemOrder.objects.create(order_id=order.id, user_id=request.user.id,
                                     product_id=c.product.id, variant_id=c.variant.id, quantity=c.quantity)



        Cart.objects.filter(user_id=request.user.id).delete()
        return redirect('order:order_details', order.id)


        # if form.is_valid():
        #     print('ok')
        #     data = form.cleaned_data
        #     code = get_random_string(length=8)
        #     order = Order.objects.create(user_id = request.user.id,email=data['email'],
        #                                  f_name=data['f_name'],l_name=data['l_name'],address=data['address'],zipcode=data['zipcode'],code=code,phone=data['phone'])
        #     cart = Cart.objects.filter(user_id=request.user.id)
        #     for c in cart:
        #         ItemOrder.objects.create(order_id=order.id,user_id=request.user.id,
        #                                  product_id=c.product.id,variant_id=c.variant.id,quantity=c.quantity)
        #     Cart.objects.filter(user_id=request.user.id).delete()
        #     return redirect('order:order_details',order.id)

@require_POST
def coupon_order(request,order_id):
    form = CouponForm(request.POST)
    time = jdatetime.datetime.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,start__lte=time,end__gte=time,active=True)
        except Coupon.DoesNotExist:
            messages.error(request,"کد وارد شده معتبر نیست",'danger')
            return redirect('order:order_details',order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return  redirect('order:order_details',order_id)



MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:127.0.0.1:8000/order:verify/'


def send_request(request,price,order_id):
    global amount,id
    id = order_id
    amount = price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": request.user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    # authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        pass
        # return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        cart = ItemOrder.objects.filter(order_id = order_id)
        for c in cart:
            if c.product.status == 'None':
                product = Product.objects.get(id=c.product.id)
                product.sell += c.quantity
                product.amount -= c.quantity
                product.save()
                code = order.code
                phone = f"0{request.user.profile.phone}"
                sms = ghasedak.Ghasedak("0c2eba3047039348177a1565837633b259a2bb076dc12bbb414bcb61004f87ab")
                sms.send({'message': code, 'receptor': phone, 'linenumber': "10008566"})
            else:

                variant = Variants.objects.get(id=c.variant.id)
                product.sell += c.quantity
                variant.amount  -= c.quantity
                variant.save()
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('Transaction success')
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')


if pg_api.PIN == 'sandbox':
    PG_URL = 'https://panel.aqayepardakht.ir/startpay/sandbox/'
else:
    PG_URL = 'https://panel.aqayepardakht.ir/startpay/'

@login_required(login_url='accounts:login')
def delivery(request,order_id):
    order = Order.objects.filter(id=order_id, paid=False,user_confirmed=False).first()
    if order:
        if request.method == 'POST':
            with disable_signals(pre_save):
                order.user_confirmed=True
                order.save()
            products = ItemOrder.objects.filter(order_id=order.pk)
            for item in products:
                if item.product.status == 'None':
                    if p := Product.objects.filter(id=item.product.pk).first():
                        p.amount -= item.quantity
                        p.sell += item.quantity
                        p.save()
                else:
                    if v := Variants.objects.filter(id=item.variant.pk).first():
                        v.amount -= item.quantity
                        v.save()

            messages.success(request, 'سفارش با موفقیت ثبت شد همکاران ما با شما تماس خواهند گرفت ', 'success')
            return redirect('home:home')
        form = CouponForm()
        if not order.tipax:
            items = order.order_item.all()
            weight = 0
            for i in items:
                weight += i.variant.weight * i.quantity

            delivery_price = get_delivery_price(weight)
        else:
            delivery_price = None

        ctx = {
            'order': order,
            'form': form,
            'delivery_price': delivery_price
        }
        return render(request,"order/delivery.html",ctx)
    messages.add_message(request, 200, 'something went wrong!', 'danger')
    return redirect('home:home')



@login_required(login_url='accounts:login')
def cart_to_cart(request,order_id):
    order = Order.objects.filter(id=order_id, paid=False,user_confirmed=False).first()
    if order:
        cartform=CartForm(request.POST or None, request.FILES or None, instance=order)
        if cartform.is_valid():
            obj=cartform.save(commit=False)
            with disable_signals(pre_save):
                obj.user_confirmed=True
                obj.save()
            products = ItemOrder.objects.filter(order_id=obj.pk)
            for item in products:
                if item.product.status == 'None':
                    if p := Product.objects.filter(id=item.product.pk).first():
                        p.amount -= item.quantity
                        p.sell += item.quantity
                        p.save()
                else:
                    if v := Variants.objects.filter(id=item.variant.pk).first():
                        v.amount -= item.quantity
                        v.save()
            messages.success(request, 'سفارش شما پس از تایید ثبت خواهد شد ', 'success')
            return redirect('home:home')
        form = CouponForm()
        if not order.tipax:
            items = order.order_item.all()
            weight = 0
            for i in items:
                weight += i.variant.weight * i.quantity

            delivery_price = get_delivery_price(weight)
        else:
            delivery_price = None

        ctx = {
            'order': order,
            'form': form,
            'cartform':cartform,
            'delivery_price': delivery_price
        }
        return render(request,"order/cart_to_cart.html",ctx)

    messages.add_message(request, 200, 'سفارش یافت نشد', 'danger')
    return redirect('home:home')  

class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            if order := Order.objects.filter(id=order_id, paid=False).first():
                form = CouponForm()

                if not order.tipax:
                    items = order.order_item.all()
                    weight = 0
                    for i in items:
                        weight += i.variant.weight * i.quantity

                    delivery_price = get_delivery_price(weight)
                else:
                    delivery_price = None

                ctx = {
                    'order': order,
                    'form': form,
                    'delivery_price': delivery_price
                }

                return render(request, 'order/order.html', ctx)

            messages.add_message(request, 200, 'order not found', 'warning')
            return redirect('home:home')

        except Exception as e:
            save_log(request, 'ERR_GET', e)
            messages.add_message(request, 200, 'an error occurred. please try again')
            return redirect('home:home')

    def post(self, request, order_id):
        try:
            if order := Order.objects.filter(id=order_id, paid=False).first():
                data = {
                    'amount': str(order.get_price()),
                    'invoice_id': order.code
                }

                response = pg_api.pg_get_trans_id(data)
                res = response.json()

                if response.status_code == 200:
                    if res.get('status') == 'success':
                        pg_url = f'{PG_URL}{res.get("transid")}/'

                        return HttpResponseRedirect(pg_url)

                    save_log(request, 'ERR_POST_PG', res.get('code'), data)
                    messages.add_message(request, 200, 'something went wrong!', 'danger')
                    return redirect('home:home')

                err = pg_api.pg_get_err(res.get('code'))
                save_log(request, 'ERR_POST_PG', f'خطا:{err}\ncode: {res.get("code")}', data)
                messages.add_message(request, 200, 'something went wrong!', 'danger')
                return redirect('home:home')

            messages.add_message(request, 200, 'order not found')
            return redirect('home:home')

        except Exception as e:
            save_log(request, 'ERR_POST', e)
            messages.add_message(request, 200, 'an error occurred. please try again')
            return redirect('home:home')


class OrderReserve(LoginRequiredMixin, View):
    def post(self, request, *args):
        try:
            form = OrderForm(request.POST)
            hours = request.POST.get('hours')
            payment_method = request.POST.get('payment_method')
            delivery = request.POST.get('delivery')
            print(delivery)
            if form.is_valid():
                t_code = str(uuid.uuid4())
                order = form.save(commit=False)
                order.user = request.user
                order.code = t_code
                if order.city.id == 1:
                    if hours and hours != '0':
                        dh = DeliveryHour.objects.filter(id=hours).first()
                        order.delivery_hour = dh
                    if payment_method and payment_method == '1':
                        order.payment_method = '1'
                    elif payment_method and payment_method == '2':
                        order.payment_method = '2'
                        order.user_confirmed=False
                    elif payment_method and payment_method == '3':
                        order.payment_method = '3'
                        order.user_confirmed=False
                    else:
                        order.payment_method = '1'
                
                if delivery and delivery == 'tipax':
                    order.tipax = True

                with disable_signals(pre_save):
                    order.save()

                items = Cart.objects.filter(user=request.user)
                for i in items:
                    ItemOrder.objects.create(
                        order_id=order.pk,
                        user_id=request.user.pk,
                        product_id=i.product.pk if i.product else None,
                        variant_id=i.variant.pk if i.variant else None,
                        quantity=i.quantity
                    )
                items.delete()
                if order.payment_method == '2':
                    return redirect(f"/order/delivery/{order.id}")
                elif order.payment_method == '3':
                    return redirect(f"/order/cart_to_cart/{order.id}")
                else:
                    return redirect('order:order_details', order.pk)
            save_log(request, 'ERR_POST', form.errors, request.POST)
            return render(request, 'cart/cart.html', {'form': form})

        except Exception as e:
            save_log(request, 'ERR_POST', e)
            messages.add_message(request, 200, 'an error occurred. please try again')
            return redirect('home:home')


@method_decorator(csrf_exempt, name='dispatch')
class VerifyPayment(View):
    def post(self, request, *args):
        try:
            data = request.POST
            if order := Order.objects.filter(code=data.get('invoice_id')).first():
                check_out = CheckOut.objects.create(
                    order_id=order.pk,
                    creditNumberCard=data.get('cardnumber'),
                    date=timezone.now(),
                    trackingCode=data.get('tracking_number'),
                    trans_id=data.get('transid'),
                    invoice_id=data.get('invoice_id'),
                    bank=data.get('bank'),
                    status=data.get('status'),
                    finalPrice=order.get_price()
                )

                data = {
                    'amount': str(order.get_price()),
                    'transid': data.get('transid')
                }

                response = pg_api.pg_verify(data)
                res = response.json()

                if response.status_code == 200:
                    if res.get('status') == 'success' and res.get('code') == '1':
                        order.paid = True
                        order.save()

                        products = ItemOrder.objects.filter(order_id=order.pk)
                        for item in products:
                            if item.product.status == 'None':
                                if p := Product.objects.filter(id=item.product.pk).first():
                                    p.amount -= item.quantity
                                    p.sell += item.quantity
                                    p.save()
                            else:
                                if v := Variants.objects.filter(id=item.variant.pk).first():
                                    v.amount -= item.quantity
                                    v.save()

                        ctx = {
                            'order': order,
                            'check_out': check_out
                        }

                        return render(request, 'order/after-payment.html', ctx)

                    save_log(request, 'ERR_POST', res.get('code'), data)
                    ctx = {
                        'order': order,
                        'check_out': check_out
                    }

                    return render(request, 'order/after-payment.html', ctx)

                err = pg_api.pg_get_pay_err(res.get('code'))
                save_log(request, 'ERR_POST_PG', f'خطا:{err}\ncode: {res.get("code")}', data)
                ctx = {
                    'order': order,
                    'check_out': check_out
                }

                return render(request, 'order/after-payment.html', ctx)

        except Exception as e:
            save_log(request, 'ERR_POST', e)
            messages.add_message(request, 200, 'an error occurred! please call support.')
            return redirect('home:home')
