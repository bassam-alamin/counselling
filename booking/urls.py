from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # /home/
    path(r'', views.home.as_view(), name='home'),
    # /home/user/id ...to display userdetails
    path(r'user/(?P<pk>[0-9]+)', views.UserDetails.as_view(), name='user-details'),
    path(r'(?P<pk>[0-9]+)/(?P<slug>[\w.@+-]+)', views.UserProfile.as_view(), name='user-profile'),
    path(r'book', views.Session.as_view(), name='book'),
    #url to see schedule for counsellor
    # url(r'^reservations/(?P<pk>[0-9]+)/$', views.CounsellorBookings.as_view(), name='counsellor-bookings'),

    path(r'^reservations/(?P<pk>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.details.as_view(), name='bookings'),
    path(r'^(?P<pk>[0-9]+)/(?P<slug>[\w.@+-]+)/confirmed/$', views.confirmed.as_view(), name='confirmed'),
    path(r'^delete/(?P<pk>[0-9]+)/$', views.BookingDelete.as_view(), name='delete'),
    path(r'^confirm/(?P<pk>[0-9]+)/$', views.ConfirmBooking.as_view(), name='confirm'),

    path(r'^register/$', views.UserFormView.as_view(), name='register'),

    path(r'^login/$', views.LoginUser.as_view(), name='login'),
    path(r'^update_profile/(?P<pk>[0-9]+)/', views.UserProfileUpdate.as_view(), name='update_profile'),
    path(r'^password/$', views.change_password, name='change_password'),

    path(r'^logout/$', views.logoutuser, name='logout'),

]
