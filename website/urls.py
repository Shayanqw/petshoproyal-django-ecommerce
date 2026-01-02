
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.sitemaps import ProductViewSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'product' : ProductViewSitemap,
}


urlpatterns = [


  path('admin/', admin.site.urls),
  path('', include('home.urls', namespace='home')),
  path('accounts/', include('accounts.urls', namespace='accounts')),
  path('ckeditor/', include('ckeditor_uploader.urls')),
  path('cart/', include('cart.urls', namespace='cart')),
  path('order/', include('order.urls', namespace='order')),
  path('sitemaps.xml',sitemap,{'sitemaps':sitemaps})

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
