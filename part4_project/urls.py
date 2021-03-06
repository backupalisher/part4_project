"""part4_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from .apps.sitemap import All

sitemaps = {
    'all': All,
}

urlpatterns = [
                  path('', include('main.urls')),
                  path('404', include('main.urls')),
                  path('admin/', admin.site.urls),
                  path('search/', include('main.urls')),
                  path('about/', include('about.urls')),
                  path('contacts/', include('contacts.urls')),
                  path('auth/', include('user_passport.urls')),
                  path('cabinet/', include('user_passport.urls')),
                  path('model/', include('model.urls')),
                  path('detail/', include('detail.urls')),
                  path('brand/', include('brand.urls')),
                  path('filter/', include('filter.urls')),
                  path('cartridge/', include('cartridge.urls')),
                  path('sendmail/', include('sendmail.urls')),
                  # path('api/v1/brands/', include('brand.urls')),
                  # path('api/v1/models/', include('model.urls')),
                  # path('api/v1/cartridges/', include('cartridge.urls')),
                  # path('api/v1/details/', include('detail.urls')),
                  path('account/', include('accounts.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # urlpatterns += [path(r'^silk/', include('silk.urls', namespace='silk'))]

    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
# + static(settings.STATIC_URL, document_root=settings.STATIC_URL) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
