from contextlib import contextmanager
from django.db.models.signals import post_save, post_delete,pre_save
from .models import Order,ItemOrder
from django.dispatch import receiver
from .models import Product,Variants

@receiver(pre_save, sender=Order)
def handle_order_confirmation_change(sender, instance, **kwargs):
    if instance.pk:
        previous_order = Order.objects.get(pk=instance.pk)
        if instance.payment_method == Order.CART_TO_CART:
              #   release the product quantity
            if previous_order.user_confirmed and not instance.user_confirmed:
                products = ItemOrder.objects.filter(order_id=instance.pk)
                for item in products:
                    if item.product.status == 'None':
                        if p := Product.objects.filter(id=item.product.pk).first():
                            p.amount += item.quantity
                            p.sell -= item.quantity
                            p.save()
                    else:
                        if v := Variants.objects.filter(id=item.variant.pk).first():
                            v.amount += item.quantity
                            v.save()
            
    

@contextmanager
def disable_signals(*signals):
    for signal in signals:
        signal.disconnect(sender=Order)
    try:
        yield
    finally:
        for signal in signals:
            signal.connect(handle_order_confirmation_change, sender=Order)