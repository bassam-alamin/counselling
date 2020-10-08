from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from booking.views import home1




urlpatterns = [
    url(r'^admin/', admin.site.urls,name='admin'),
    url(r'^home/',include('booking.urls')),
    url(r'^$',home1.as_view(),name='home1'),


]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)