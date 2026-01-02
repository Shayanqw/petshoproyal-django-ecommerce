from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_details, name="details"),
    path("add/<int:id>/", views.cart_add, name="add_cart"),
    path("remove/<int:id>/", views.cart_remove, name="remove"),
    path("show/", views.cart_show, name="show"),
    path("add-single/<int:id>/", views.add_single, name="add-single"),
    path("remove_single/<int:id>/", views.remove_single, name="remove_single"),
    path("update-cart", views.updatecart, name="updatecart"),
    path("provinces-json/", views.get_json_province_data, name="provinces-json"),
    path("city-json/<str:city>/", views.get_json_city_data, name="models-json"),
    path("cart-count/", views.ItemcountView.as_view(), name="cart-count"),
]
