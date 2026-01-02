from django.shortcuts import render,get_object_or_404,redirect
from urllib3 import request

from .models import *
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from cart.forms import *
from django.db.models import Q,Max,Min,Count,Sum
from cart.models import *
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from .filters import ProductFilter
from urllib.parse import urlencode
from .compare import Compare
from django.http import JsonResponse
from django.db.models import Case, When, Value, IntegerField

def home(request):
    category = Category.objects.filter(sub_cat=False)
    gallery = Gallery.objects.all()
    
    # Annotate each product with an "availability_order" field:
    # available products (amount != 0) get 0 and unavailable (amount == 0) get 1.
    create = Product.objects.annotate(
        availability_order=Case(
            When(amount=0, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    ).order_by('availability_order', '-create')
    
    max_discount = Product.objects.all().order_by('-discount')[:6]
    nums = Cart.objects.filter(user_id=request.user.id).aggregate(sum=Sum('quantity'))['sum']
    latest_blogs = Blog.objects.all().order_by('-published_date')[:3]
    return render(request, 'home/home.html', {
        'max_discount': max_discount,
        'category': category,
        'gallery': gallery,
        'create': create,
        'nums': nums,
        'latest_blogs': latest_blogs,
    })
# def home(request):
#     category = Category.objects.filter(sub_cat=False)
#     gallery = Gallery.objects.all()
#     # create = Variants.objects.all().order_by('-create')[:6]
#     # create = Variants.objects.all()
#     # max_discount = Variants.objects.all().order_by('-discount')[:6]
#     create = Product.objects.all()
#     max_discount = Product.objects.all().order_by('-discount')[:6]
#     nums = Cart.objects.filter(user_id=request.user.id).aggregate(sum=Sum('quantity'))['sum']
#     return render(request,'home/home.html',{'max_discount':max_discount,'category':category,'gallery':gallery,'create':create,
#                                             'nums':nums})

def all_product(request,slug=None,id=None):
    products = Product.objects.all()
    variant = Variants.objects.all()
    price_agg = Product.objects.aggregate(
    min_price=Min('unit_price'),
    max_price=Max('unit_price'),)

    min_price = int(price_agg.get('min_price') or 0)
    max_price = int(price_agg.get('max_price') or 0)

    filter = ProductFilter(request.GET,queryset=products)
    products = filter.qs
    paginator = Paginator(products,8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    category = Category.objects.filter(sub_cat=False)

    if slug and id:
        data = get_object_or_404(Category,slug=slug,id=id)
        page_obj = products.filter(category=data)
        paginator = Paginator(page_obj, 8)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
    s_form = SearchForm()
    if 'search' in request.GET:
        s_form = SearchForm(request.GET)
        if s_form.is_valid():
            info = s_form.cleaned_data['search']
            page_obj = products.filter(Q(name__icontains=info))
            paginator = Paginator(page_obj, 8)
            page_num = request.GET.get('page')
            data = request.GET.copy()
            if 'page' in data:
                del data['page']
            page_obj = Paginator.get_page(page_num)



    return render(request,'home/product.html',{'variant':variant,'products':page_obj,'category':category,'s_form':s_form,
                                               'page_num':page_num,'filter':filter,'min_price':min_price,'max_price':max_price,
                                              })

def product_detail(request,id):
    product = get_object_or_404(Product,id=id)
    form = CartAddForm()
    ip = request.META.get('REMOTE_ADDR')
    view = Views.objects.filter(product_id=product.id,ip=ip)
    if not view.exists():
        Views.objects.create(product_id=product.id,ip=ip)
        product.num_view +=1
        product.save()
    if request.user.is_authenticated:
        product.view.add(request.user)
    update = Chart.objects.filter(product_id=id)
    change = Chart.objects.all()
    images = Images.objects.filter(product_id=id)
    comment_form = CommentForm()
    reply_form = ReplayForm()
    cart_form = CartForm()
    comment = Commnet.objects.filter(product_id=id,is_reply=False)
    similar = product.tags.similar_objects()[:2]
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite=True
    is_like =False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True


    if product.status != 'None':
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variants.objects.get(id=var_id)
            colors = Variants.objects.filter(product_variant_id=id,size_variant_id=variants.size_variant_id)
            size= Variants.objects.raw(
                'SELECT * FROM home_variants WHERE product_variant_id=%s GROUP BY size_variant_id',[id])

            # sizes = Variants.objects.filter(product_variant_id=id).distinct('size_variant_id') #for postgresql
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)
            colors = Variants.objects.filter(product_variant_id=id, size_variant_id=variants.size_variant_id)
            size = Variants.objects.raw(
                'SELECT * FROM home_variants WHERE product_variant_id=%s GROUP BY size_variant_id', [id])

        context = {'product':product,'variant':variant,'variants':variants,'similar':similar,'is_like':is_like,'comment_form':comment_form,
                   'comment':comment,'reply_form':reply_form,'images':images,'is_unlike':is_unlike,'cart_form':cart_form,'is_favourite':is_favourite,'change':change,'colors':colors,'size':size,'form':form}
        return render(request, 'home/details.html', context)
    else:
        return render(request,'home/details.html',{'product':product,'similar':similar,
                                                   'is_like':is_like,'comment_form':comment_form,'comment':comment,'reply_form':reply_form,
                                                   'images':images,'is_unlike':is_unlike,'cart_form':cart_form,'is_favourite':is_favourite,'update':update,'form':form})


def product_like(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product,id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
        messages.success(request,'remove','success')
    else:
        product.like.add(request.user)
        is_like = True
        messages.success(request, 'add', 'success')
    return redirect(url)


def product_unlike(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product,id=id)
    product.unlike.add(request.user)
    messages.success(request, 'add like', 'dark')
    return redirect(url)




def product_Comment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_Form = CommentForm(request.POST)
        if comment_Form.is_valid():
            data = comment_Form.cleaned_data
            Commnet.objects.create(comment=data['comment'],rate=data['rate'],user_id=request.user.id,product_id=id)
        return redirect(url)

def product_reply(request,id,comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplayForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Commnet.objects.create(comment=data['comment'],product_id=id,user_id=request.user.id,reply_id=comment_id,is_reply=True)
            messages.success(request,'tnx for reply','primary')
            return redirect(url)

def comment_like(request,id):
    url = request.META.get('HTTP_REFERER')
    comment = Commnet.objects.get(id=id)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
    else:
        comment.comment_like.add(request.user)
        messages.success(request,'tnx for like','warning')
    return JsonResponse({'success':'ok'})


def product_search(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = products.filter(Q(discount__exact=data)|Q(unit_price__exact=data))
            else:
                products = products.filter(Q(name__icontains=data))
            return render(request,'home/product.html',{'products':products,'form':form})



def favourite_product(request,id):
    url =request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        product.total_favourite -=1
        product.save()
        is_favourite = False
    else:
        product.favourite.add(request.user)
        product.total_favourite += 1
        product.save()
        is_favourite = True
    return redirect(url)

def contact(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        msg = request.POST['message']
        body = subject + '\n' + email + '\n' + msg
        form = EmailMessage(
            'Contact Form',
            body,
            'test',
            ('paneldjango@gmail.com',),
        )
        form.send(fail_silently=False)
    return render(request,'home/contact.html')



def compare(request):
    data = Compare(request)
    return render(request,'home/compare.html',{'data':data})

def about(request):
    return render(request,'home/about.html')

def add_compare(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    data = Compare(request)
    data.add(product=product)
    return redirect('home:compare')

def remove_compare(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    data = Compare(request)
    data.remove(product=product)
    return redirect('home:compare')


def favourite_product(request,id):
    # url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product,id=id)
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
    else:
        product.favourite.add(request.user)
    product.save()
    return JsonResponse({'success' : 'html'})




def blog_list(request):
    blogs = Blog.objects.all().order_by('-published_date')
    return render(request, 'home/blog.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog_post = get_object_or_404(Blog, pk=pk)
    return render(request, 'home/blog_detail.html', {'blog': blog_post})




