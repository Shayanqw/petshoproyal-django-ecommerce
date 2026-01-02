from django.shortcuts import render, redirect, get_object_or_404
from home.models import *
from .models import *
from order.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
# from .cart import Cart
from .forms import CartAddForm
from django.http import JsonResponse, Http404
from django.views.generic.base import View


@login_required(login_url='accounts:login')
def cart_details(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    form = OrderForm()
    qs = Province.objects.all()
    user = request.user
    total = 0
    hours = DeliveryHour.objects.all()
    for p in cart:
        if p.product.status != 'None':
            total += p.variant.total_price * p.quantity
        else:
            total += p.product.total_price * p.quantity
    return render(request, 'cart/cart.html', {'cart': cart, 'total': total, 'form': form, 'user': user, 'qs': qs, 'hours': hours})


def get_json_province_data(request):
    qs_val = list(Province.objects.values())
    return JsonResponse({'data': qs_val})


def get_json_city_data(request, *args, **kwargs):
    selected_province = kwargs.get('city')
    obj_cities = list(City.objects.filter(province_id=selected_province).values())
    return JsonResponse({'data': obj_cities})


@login_required(login_url='accounts:login')
def cart_add(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.status != 'None':
        var_id = request.POST.get('select')
        data = Cart.objects.filter(user_id=request.user.id, variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id=request.user.id, product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    if request.method == 'POST':
        form = CartForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status != 'None':
                    shop = Cart.objects.get(user_id=request.user.id, product_id=id, variant_id=var_id)
                else:
                    shop = Cart.objects.get(user_id=request.user.id, product_id=id)
                shop.quantity += info
                shop.save()
            else:
                Cart.objects.create(user_id=request.user.id, product_id=id, variant_id=var_id, quantity=info)
        messages.success(request,'کالای شما با موفقیت به سبد خرید اضافه شد','success')
        return redirect(url)


def cart_remove(request, id):
    # url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    # return (url)
    return redirect('cart:details')


def cart_show(request):
    total, price, quantity, discount = 0, 0, 0, 0
    cart = Cart.objects.get(user_id=request.user.id)
    # for c in cart:
    #     total += int(c['variant'].total_price * c['quantity'])
    #     price += int(c['variant'].unit_price * c['quantity'])
    #     quantity += c['quantity']
    #     discount = price - total
    response = {'total': total, 'price': price, 'quantity': quantity, 'discount': discount}
    return JsonResponse(response)


def add_single(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.product.status == 'None':
        product = Product.objects.get(id=cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity += 1
    else:
        variant = Variants.objects.get(id=cart.variant.id)
        if variant.amount > cart.quantity:
            cart.quantity += 1
    cart.save()
    return redirect(url)


def remove_single(request):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)


def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=request.user, variant_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(variant_id=prod_id, user=request.user)
            print(prod_qty)
            cart.quantity = prod_qty
            cart.save()
            return JsonResponse({'status': "updated successfully"})
    return redirect('/')


class ItemcountView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user_id=request.user.id)
        count = cart.count()
        request.session['cart_item_count'] = count

        return JsonResponse({"count": count})

#
# def cart_details(request):
#     cart = Cart.objects.filter(user_id=request.user.id)
#     user = request.user
#     form = OrderForm()
#     total=0
#     for p in cart:
#         if p.product.status != 'None':
#             total += p.variant.total_price * p.quantity
#         else:
#             total += p.product.total_price * p.quantity
#     return render(request,'cart/cart.html',{'cart':cart,'total':total,'form':form,'user':user})
#
# @login_required(login_url='accounts:login')
# def add_cart(request,id):
#     url = request.META.get('HTTP_REFERER')
#     product = Product.objects.get(id=id)
#     if product.status != 'None':
#         var_id = request.POST.get('select')
#         data = Cart.objects.filter(user_id=request.user.id,variant_id=var_id)
#         if data :
#             check = 'yes'
#         else:
#             check = 'no'
#     else:
#         data = Cart.objects.filter(user_id=request.user.id,product_id=id)
#         if data:
#             check ='yes'
#         else:
#             check = 'no'
#     if request.method == 'POST':
#         form = CartForm(request.POST)
#         var_id = request.POST.get('select')
#         if form.is_valid():
#             info = form.cleaned_data['quantity']
#             if check == 'yes':
#                 if product.status !='None':
#                     shop = Cart.objects.get(user_id = request.user.id,product_id=id,variant_id=var_id)
#                 else:
#                     shop = Cart.objects.get(user_id=request.user.id, product_id=id)
#                 shop.quantity = info
#                 shop.save()
#             else :
#                 Cart.objects.create(user_id=request.user.id,product_id=id,variant_id=var_id,quantity=info)
#         return redirect(url)
#
#
# @login_required(login_url='accounts:login')
# def remove_cart(request,id):
#     url = request.META.get('HTTP_REFERER')
#     Cart.objects.filter(id=id).delete()
#     return redirect(url)
#
# def add_single(request,id):
#     url = request.META.get('HTTP_REFERER')
#     cart = Cart.objects.get(id=id)
#     if cart.product.status =='None':
#         product = Product.objects.get(id=cart.product.id)
#         if product.amount > cart.quantity:
#             cart.quantity += 1
#     else :
#         variant = Variants.objects.get(id=cart.variant.id)
#         if variant.amount > cart.quantity :
#             cart.quantity += 1
#     cart.save()
#     return redirect(url)
#
# def remove_single(request,id):
#     url = request.META.get('HTTP_REFERER')
#     cart = Cart.objects.get(id=id)
#     if cart.quantity < 2:
#         cart.delete()
#     else:
#         cart.quantity -= 1
#         cart.save()
#     return redirect(url)
#
# def compare(request,id):
#     url = request.META.get('HTTP_REFERER')
#     if request.user.is_authenticated:
#         item = get_object_or_404(Product,id=id)
#         qs = Compare.objects.filter(user_id=request.user.id,product_id=id)
#         if qs.exists():
#             messages.success(request,'ok user')
#         else :
#             Compare.objects.create(user_id=request.user.id,product_id=item.id,session_key=None)
#     else:
#         item = get_object_or_404(Product, id=id)
#         qs = Compare.objects.filter(user_id=None, product_id=id,session_key=request.session.session_key)
#         if qs.exists():
#             messages.success("ok session")
#         else :
#             if not request.session.session_key :
#                 request.session.create()
#             Compare.objects.create(user_id=None,product_id=item.id,session_key=request.session.session_key)
#     return redirect(url)
#
#
# def show(request):
#     if request.user.is_authenticated:
#         data = Compare.objects.filter(user_id=request.user.id)
#         return render(request,'cart/show.html', {'data': data})
#     else:
#         data = Compare.objects.filter(session_key__exact=request.session.session_key,user_id=None)
#         return render(request, 'cart/show.html', {'data': data})
#
