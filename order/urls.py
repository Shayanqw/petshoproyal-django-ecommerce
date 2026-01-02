from django.urls import path

from . import views

app_name = 'order'
urlpatterns = [
    # path('<int:order_id>/', views.order_details, name='order_details'),
    # path('create/',views.order_create,name='order_create'),
    path('coupon/<int:order_id>/', views.coupon_order, name='coupon'),
    # path('request/<int:order_id>/<int:price>/', views.send_request, name='request'),
    # path('verify/',views.verify,name='verify'),
    path('<int:order_id>/', views.OrderDetail.as_view(), name='order_details'),
    path('create/', views.OrderReserve.as_view(), name='order_create'),
    path('verify-payment/', views.VerifyPayment.as_view()),
    path('cart_to_cart/<int:order_id>',views.cart_to_cart),
    path('delivery/<int:order_id>',views.delivery)
    
]
