from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from booking.views import home1




urlpatterns = [
    path(r'^admin/', admin.site.urls,name='admin'),
    path(r'^home/',include('booking.urls')),
    path(r'^$',home1.as_view(),name='home1'),


]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)