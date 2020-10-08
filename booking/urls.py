from django.conf.urls import url
from . import views

app_name = 'booking'

urlpatterns = [
    # /home/
    url(r'^$', views.home.as_view(), name='home'),
    # /home/user/id ...to display userdetails
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetails.as_view(), name='user-details'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.UserProfile.as_view(), name='user-profile'),
    url(r'^book$', views.Session.as_view(), name='book'),
    #url to see schedule for counsellor
    # url(r'^reservations/(?P<pk>[0-9]+)/$', views.CounsellorBookings.as_view(), name='counsellor-bookings'),

    url(r'^reservations/(?P<pk>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.details.as_view(), name='bookings'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w.@+-]+)/confirmed/$', views.confirmed.as_view(), name='confirmed'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.BookingDelete.as_view(), name='delete'),
    url(r'^confirm/(?P<pk>[0-9]+)/$', views.ConfirmBooking.as_view(), name='confirm'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^login/$', views.LoginUser.as_view(), name='login'),
    url(r'^update_profile/(?P<pk>[0-9]+)/', views.UserProfileUpdate.as_view(), name='update_profile'),
    url(r'^password/$', views.change_password, name='change_password'),

    url(r'^logout/$', views.logoutuser, name='logout'),

]
