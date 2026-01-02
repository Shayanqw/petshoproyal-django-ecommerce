from django.urls import path

from . import views

app_name='home'
urlpatterns = [
    path('',views.home,name='home'),
    path('product/',views.all_product,name='product'),
    path('detail/<int:id>/',views.product_detail,name='detail'),
    path('category/<slug>/<int:id>',views.all_product,name='category'),
    path('like/<int:id>',views.product_like,name='product_like'),
    path('unlike/<int:id>',views.product_unlike,name='product_unlike'),
    path('comment/<int:id>',views.product_Comment,name='product_Comment'),
    path('reply/<int:id>/<int:comment_id>/',views.product_reply,name='product_reply'),
    path('like_comment/<int:id>',views.comment_like,name='comment_like'),
    path('search/',views.product_search,name='product_search'),
    path('favourite/<int:id>/',views.favourite_product,name='favourite'),
    path('contact/',views.contact,name='contact'),
    path('compare/',views.compare,name='compare'),
    path('about/',views.about,name='about'),
    path('add/<int:product_id>',views.add_compare,name='add'),
    path('remove/<int:product_id>',views.remove_compare,name='remove'),
    path('favourite/<int:id>', views.favourite_product, name='favourite'),
    path('blogs/', views.blog_list, name='blog_list'),  # A page listing all blogs
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),  # Detailed view for each blog
]
