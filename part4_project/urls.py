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
from django.urls import path, include, re_path
from django.contrib.sitemaps.views import sitemap

from .apps.sitemap import All

sitemaps = {
    'all': All,
}
urlpatterns = [
                  re_path(r'^i18n/', include('django.conf.urls.i18n')),
                  path('', include('main_views.urls')),
                  path('404', include('main_views.urls')),
                  path('auth/', include('user_passport.urls')),
                  path('cabinet/', include('user_passport.urls')),
                  path('sendmail/', include('sendmail.urls')),
                  path('account/', include('accounts.urls')),
                  path('dashboard/', include('dashboard.urls')),
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
