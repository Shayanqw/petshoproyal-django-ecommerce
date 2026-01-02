from django import forms
from .models import Order,CheckOut
from django.core.exceptions import ValidationError

class CartForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['tracking_code', 'payment_screenshot']
        widgets = {
            'tracking_code': forms.TextInput(attrs={'class': 'form-control',"id":"id_trackingCode", 'placeholder': 'شماره پیگیری یا شماره ارجاع 12 رقمی','required': 'required',}),
            'payment_screenshot': forms.ClearableFileInput(attrs={'class': 'form-control','id':'id_screenshot','placeholder': 'اپلود اسکرین شات','required': 'required',}),
        }

    def clean_tracking_code(self):
            tracking_code = self.cleaned_data.get('tracking_code')
            
            if not tracking_code:
                raise ValidationError('شماره پیگیری یا شماره ارجاع الزامی است.')

            if len(tracking_code) != 12:
                raise ValidationError('شماره پیگیری باید 12 رقم باشد.')

            return tracking_code
        
    def clean_payment_screenshot(self):
            payment_screenshot = self.cleaned_data.get('payment_screenshot')
            
            if not payment_screenshot:
                raise ValidationError('آپلود اسکرین شات الزامی است.')

            return payment_screenshot


class CouponForm(forms.Form):
    code = forms.CharField(max_length=100)


class CheckOutForm(forms.ModelForm):
    # PAYMENT_METHOD_CHOICES = [
    #     ('online','Online Payment'),
    #     ('cash','Cash Payment'),
    # ]
    # payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES,widget=forms.RadioSelect )    
    class Meta:
        model = CheckOut
        fields = ['creditNumberCard','date','trackingCode']
