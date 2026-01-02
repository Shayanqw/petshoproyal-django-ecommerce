from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator




phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="Phone number must start with 09 and be exactly 11 digits long."
)



error = {
    'min_length':'tedad kam ast',
    'required':'elzam b por boudan',
}


class UserRegisterForm(forms.Form):
    # user_name=forms.CharField(error_messages=error,max_length=200,widget=forms.TextInput(attrs={'placeholder':'نام کاربری خود را وارد نمایید'}))
    # email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'enter email...'}))
    first_name=forms.CharField(max_length=10,min_length=3,error_messages=error)
    last_name=forms.CharField(max_length=200)
    # password_1=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder' : 'plz pass...'}))
    # password_2=forms.CharField(max_length=200)
    phone=forms.CharField(max_length=11,required=True,validators=[phone_validator],widget=forms.TextInput(attrs={'placeholder':'تلفن خود را وارد کنید',}))
    otpcode=forms.IntegerField(required=True)

   
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('شماره تلفن تکراری است')
        return phone
    

    # def clean_email(self):
    #      email = self.cleaned_data['email']
    #      if User.objects.filter(email=email).exists():
    #          raise forms.ValidationError('email tekrari ast')
    #      return email


    # def clean_password_2(self):
    #     password1 = self.cleaned_data['password_1']
    #     password2 = self.cleaned_data['password_2']
    #     if password1 != password2 :
    #         raise forms.ValidationError('password not match')
    #     # elif len(password2) < 8:
    #     #     raise forms.ValidationError('password is short')
    #     # elif not any(x.isupper() for x in password2):
    #     #     raise forms.ValidationError('hadeaghal ....')
    #     return password1


class UserLoginForm(forms.Form):
    username = forms.CharField()
    # password = forms.CharField()
    # remember = forms.BooleanField(required=False,widget=forms.CheckboxInput())


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','address','profile_image']


class PhoneForm(forms.Form):
    phone = forms.IntegerField()


class CodeForm(forms.Form):
    code = forms.IntegerField()















class Resetpassword(forms.Form):
    password_1=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder' : 'رمز عبور را وارد کنید '}))
    password_2=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder' : ' تکرار رمز عبور را وارد کنید '}))


    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2 :
            raise forms.ValidationError('password not match')
        # elif len(password2) < 8:
        #     raise forms.ValidationError('password is short')
        # elif not any(x.isupper() for x in password2):
        #     raise forms.ValidationError('hadeaghal ....')
        return password1
