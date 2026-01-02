import pyotp
from django.shortcuts import render,redirect,reverse, get_object_or_404
from django.http import JsonResponse
from log.defines import save_log
from .forms import *
from .models import *
from order.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
from datetime import datetime, timedelta
# import ghasedak
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import ghasedakpack
from .utils import send_otp
import re



def validate_phone_number(phone):
    pattern = r"^09\d{9}$"
    
    if re.match(pattern, phone):
        return True  
    else:
        return False  


class PhoneToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

phone_generator = PhoneToken()


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

email_generator = EmailToken()


def redirect_if_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')  
        return view_func(request, *args, **kwargs)
    return wrapper


@redirect_if_authenticated
def registerotp(request):
    if request.method=="POST":
        phone = request.POST['phone']
        user=User.objects.filter(profile__phone=phone).exists()
        if validate_phone_number(phone):
            if not user:
                request.session['phone'] = phone[1:]
                send_otp(request)
                return JsonResponse({"status":200,"message":"Sent","phone":phone},status=200)
            return JsonResponse({"status":400,"message":"تلفن همراه  ثبت شده است"},status=400)
        return JsonResponse({"status":400,"message":"شماره همراه وارد شده صحیح نمی باشد "},status=400)
    return JsonResponse({"status":400,"message":"invalid method"},status=400)


def resetpassword(request,uidb64,token):
    form=Resetpassword(request.POST or None)
    id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(id=id).first() 

    if not  phone_generator.check_token(user,token) or user is None:
        return redirect("accounts:reset")
    
    if form.is_valid():
        if user and phone_generator.check_token(user,token):
            user.set_password(form.cleaned_data['password_2'])
            user.save()
            return redirect('accounts:login')
        messages.error(request,'invalid token')
        return redirect("accounts:reset")
    
    context={
        'form':form,
    }
    return render(request,"accounts/resetpass.html",context)

def resetpasswordotp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    token=phone_generator.make_token(user)
                    uid64=urlsafe_base64_encode(force_bytes(user.pk))
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['phone']

                    return redirect(f"/accounts/resetpassword/{uid64}/{token}")

            else:
                messages.error(request,'invalid one time password')
        else:
            messages.error(request,'one time password has expired')
    else:
        pass
    return render(request,'accounts/otp.html',{})


@redirect_if_authenticated
def resetpass(request):
    if request.method=="POST":
        phone = request.POST['phone']
        user=User.objects.filter(profile__phone=phone)
        if validate_phone_number(phone):
            if user.exists():
                request.session['phone'] = phone[1:]
                request.session["username"]=user.first().username
                send_otp(request)
                return redirect('accounts:resetotp')
        messages.error(request,'شماره همراه وارد شده صحیح نمی باشد ')
    context={

    }
    return render(request,"accounts/reset.html",context)

@redirect_if_authenticated
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # profile_form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            otp_code=data["otpcode"]
            otp_secret_key = request.session['otp_secret_key']
            otp_valid_until = request.session['otp_valid_date']
            if otp_secret_key and otp_valid_until is not None:
                valid_until = datetime.fromisoformat(otp_valid_until)
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=60)
                    if totp.verify(otp_code):
                        user = User.objects.create(username=data['phone'],first_name=data['first_name'],
                                     last_name=data['last_name'])
                        user.set_unusable_password() 
                        user.is_active = True
                        user.save()
                        Profile_obj = Profile.objects.filter(user=user).first()
                        Profile_obj.phone=data['phone']
                        Profile_obj.save()
                        
                        messages.warning(request, 'ثبت نام با موفقیت انجام شد. لطفا اطلاعات خود را در قسمت اطلاعات حساب تکمیل فرمایید', 'warning')
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        del request.session['phone']
                        login(request, user)
                        return redirect('accounts:profile')
            messages.error(request,'کد نامعتبراست')
        else:
            messages.warning(request, 'لطفا اطلاعات خود را صحیح وارد کنید', 'warning')

    else:
        form = UserRegisterForm()
        # profile_form = ProfileUpdateForm()

    context = { 'form':form }
    return render(request,'accounts/register.html',context)




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['username'] = username
            request.session['phone'] = Profile.objects.get(user=user).phone
            # request.session['phone'] = request.user.phone

            send_otp(request)

            return redirect('accounts:otp')
    else:
        form = UserLoginForm()
    return render(request,'accounts/login.html',{'form':form})


    #     form = UserLoginForm(request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         remember = data['remember']
    #         try:
    #             user = authenticate (request,username=User.objects.get(email=data['user']),password=data['password'])
    #         except:
    #             user = authenticate(request,username=data['user'],password=data['password'])
    #         if user is not None:
    #             login(request,user)
    #             if not remember:
    #                 request.session.set_expiry(0)
    #             else:
    #                 request.session.set_expiry(10000)
    #             messages.success(request,'خوش آمدید','primary')
    #             return redirect('home:home')
    #         else:
    #             messages.success(request,'نام کاربری یا رمز عبور اشتباه است ','danger')
    #
    # else:
    #     form = UserLoginForm()
    # return render(request,'accounts/login.html',{'form':form})

def otp_view(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['phone']

                    return redirect('home:home')

            else:
                messages.error(request,'invalid one time password')
        else:
            messages.error(request,'one time password has expired')
    else:
        pass
    return render(request,'accounts/otp.html',{})



def user_logout(request):
    logout(request)
    messages.success(request,'با موفقیت انجام شد','warning')
    return redirect('home:home')

class RegisterEmail(View):
    def get(self,request,uidb64,token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


@login_required(login_url='accunts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    data = ItemOrder.objects.filter(user_id=request.user.id)
    product = request.user.fa_user.all()
    return render(request,'accounts/profile.html',{'profile':profile,'data':data,'product':product})



@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'با موفقیت انجام شد','success')
            return redirect('accounts:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_form':user_form,'profile_form':profile_form}
    return render(request,'accounts/update.html',context)

    context = {'user_form':user_form,'profile_form':profile_form}
    return render(request,'accounts/update.html',context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'رمز عبور با موفقیت تغییر کرد','success')
            return redirect('accounts:profile')
        else:
            messages.success(request,'رمز شما کوتاه است ','danger')
            return redirect('accounts:change')
    else :
        form = PasswordChangeForm(request.user)

    return render(request,'accounts/change.html',{'form':form})






def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            if random_code == form.cleaned_data['code']:
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                login(request,user)
                messages.success(request,'سلام')
                return redirect('home:home')
            else:
                messages.error(request,'خطا')
    else:
        form=CodeForm()
    return render(request,'accounts/code.html',{'form':form})


# def favourite(request):
#     product = request.user.fa_user.all()
#     return render(request,'accounts/favourite.html',{'product':product})


def product_view(request):
    # product =Product.objects.filter(view=request.user.id)
    views = Views.objects.filter(ip=request.META.get('REMOTE_ADDR')).order_by('-create')[:2]
    return render(request,'accounts/view.html',{'views':views})



class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/link.html'

class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done.html'

class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:compelet')

class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/compelete.html'


# def history(request):
#     data = ItemOrder.objects.filter(user_id=request.user.id)
#     return render(request,'accounts/history.html',{'data':data})


"""
User login with OTP View
Mostafa Rasouli
mostafarasooli54@gmail.com
2023-12-15
"""


class LoginOTP(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request, *args):
        return render(request, self.template_name)

    def post(self, request, *args):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if cd.get('username').isdigit():
                    if prof := Profile.objects.filter(phone=cd.get('username')).first():
                        user = prof.user
                        if user:
                            request.session['username'] = prof.user.username
                            request.session['phone'] = prof.phone

                            send_otp(request)

                            return redirect('accounts:otp')

                        else:
                            messages.add_message(request, 200, 'نام کاربری یا رمز عبور اشتباه است.')
                            return redirect('accounts:login')
                # user = authenticate(request, username=cd.get('username'), password=cd.get('password'))
                # if user:
                #     request.session['username'] = cd.get('username')
                #     request.session['phone'] = Profile.objects.get(user=user).phone

                #     send_otp(request)

                #     return redirect('accounts:otp')

                # if acc := User.objects.filter(email=cd.get('username')).first():
                #     user = authenticate(request, username=acc.username, password=cd.get('password'))
                #     if user:
                #         request.session['username'] = acc.username
                #         request.session['phone'] = Profile.objects.get(user=user).phone

                #         send_otp(request)

                #         return redirect('accounts:otp')

                messages.add_message(request, 200, 'شماره تلفن یافت نشد ')
                return redirect('accounts:login')

            save_log(request, 'ERR_POST_VALIDATION', form.errors)
            messages.add_message(request, 200, 'نام کاربری یا رمز عبور اشتباه است.')
            return redirect('accounts:login')

        except Exception as e:
            save_log(request, 'ERR_POST', e)
            messages.add_message(request, 200, 'خطایی رخ داده است، لطفا مجددا تلاش نمایید.')
            return redirect('accounts:login')
