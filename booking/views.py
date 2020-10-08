from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Book, Confirmation
from django.contrib.auth import get_user_model
from .forms import LoginForm, UserForm, UserUpdate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookForm, BookForm1, ConfirmationForm
import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django import forms

User = get_user_model()

class home1(View):
    model = User
    template_name = 'booking/home2.html'

    def get(self,request):
        return render(request,self.template_name)

class home(View):
    model = User
    template_name = 'booking/home.html'

    def get(self, request):
        q1 = User.Objects.filter(groups__name='counsellor')

        return render(request, self.template_name, {'q1': q1})

    def get_slug_field(self):
        return 'user__name'


# def home(request):
#   model = Book
#  template_name ='booking/home.html'
# return render(request,template_name,{'form':model})
class details(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'booking/bookings.html'

    def get(self, request, *args, **kwargs):
        q1 = User.Objects.filter(groups__name="counsellor")
        today = datetime.datetime.now()
        form = self.model(None)
        return render(request, self.template_name, {'form': form, 'today': today, 'q1': q1})

    def get_slug_field(self):
        return 'user__name'


class confirmed(LoginRequiredMixin, generic.DetailView):
    model = Confirmation
    template_name = 'booking/confirmed.html'

    def get(self, request, *args, **kwargs):
        q1 = User.Objects.filter(groups__name="counsellor")
        today = datetime.datetime.now()

        form = self.model(None)
        return render(request, self.template_name, {'form': form, 'today': today, 'q1': q1})

    def get_slug_field(self):
        return 'user__name'



class UserDetails(generic.DetailView):
    model = User
    template_name = 'booking/details.html'

    # def get(self, request, *args, **kwargs):
    #     q1 = User.Objects.filter(groups__name="counsellor")
    #     form = self.model(None)
    #     return render(request, self.template_name, {'form':form,'q1': q1})


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'booking/user_profile.html'

    def get(self, request, *args, **kwargs):
        q1 = User.Objects.filter(groups__name="counsellor")
        return render(request, self.template_name, {'q1': q1})


class UserProfileUpdate(UpdateView):
    model = User
    form_class = UserUpdate
    template_name = 'booking/update_user.html'

    def post(self, request, *args, **kwargs):
        return redirect('booking:user-details', request.user.id)


class BookingDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('booking:home')


class ConfirmBooking(UpdateView):
    model = Book
    form_class = ConfirmationForm
    template_name = 'booking/confirm_booking.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        filters = Confirmation.objects.filter(counsellor1=form.data['counsellor1'], time=form.data['time'],
                                              date=form.data['date'])
        if filters.exists():
            messages.error(request, 'No u cannot confirm twice')
        elif request.user.is_authenticated and form.is_valid():
            session = form.save()
            session.save()
            messages.success(request, "You have already confirmed")

        return render(request, self.template_name, {'form': form, })


class Session(LoginRequiredMixin, View):
    login_url = "booking:login"
    form_class = BookForm
    template_name = 'booking/booking.html'
    q1 = User.Objects.filter(groups__name="counsellor")

    def get(self, request):
        if request.user in self.q1:
            form_class = BookForm1
            form = form_class(None)
            return render(request, self.template_name, {'form': form, 'q1': self.q1})
        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form, 'q1': self.q1})

    def post(self, request):
        if request.user in self.q1:
            form_class = BookForm1
            form = form_class(request.POST)
            filters1 = Book.objects.filter(username=form.data['username'], date=form.data['date'])

            filters = Book.objects.filter(counsellor1=form.data['counsellor1'], time=form.data['time'],
                                          date=form.data['date'])

            if filters.exists():
                messages.error(request, "the counsellor is already occupied for that time")
                print("not succesful choose another time or date")
                return redirect('booking:book')
            elif filters1.exists():
                messages.error(request, "you can not have two bookings for the same day")
                print("you already have a booking for that day")
                return redirect('booking:book')
            elif request.user.is_authenticated and form.is_valid():
                session = form.save()
                session.save()
                messages.success(request, "Booking is succesful bro")
                return redirect("booking:bookings", request.user.id, request.user.username)

            return render(request, self.template_name, {'form': form, })
        else:
            form = self.form_class(request.POST)
            filters1 = Book.objects.filter(username=request.user, date=form.data['date'])

            filters = Book.objects.filter(counsellor1=form.data['counsellor1'], time=form.data['time'],
                                          date=form.data['date'])

            if filters.exists():
                messages.error(request, "the counsellor is already occupied for that time")
                print("not succesful choose another time or date")
                return redirect('booking:book')
            elif filters1.exists():
                messages.error(request, "you can not have two bookings for the same day")
                print("you already have a booking for that day")
                return redirect('booking:book')

            elif request.user.is_authenticated and form.is_valid():
                session = form.save()
                session.username = self.request.user
                session.save()
                messages.success(request, "Booking is succesful bro")
                return redirect("booking:bookings", request.user.id, request.user.username)

            return render(request, self.template_name, {'form': form, })


class UserFormView(View):
    form_class = UserForm
    template_name = 'booking/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = form.save()

            reg_no = form.cleaned_data['reg_no']
            password = form.cleaned_data['password']
            user.set_password(password)
            group = Group.objects.get(name='normal')
            user.groups.add(group)
            user.save()

            user = authenticate(reg_no=reg_no, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('booking:login')

        return render(request, self.template_name, {'form': form})


class LoginUser(View):
    template_name = 'booking/login_form.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        reg_no = request.POST['reg_no']
        password = request.POST['password']

        user = authenticate(reg_no=reg_no, password=password)
        if user is None:
            user_queryset = User.Objects.filter(phone_no=form.data['reg_no'])
            print(user_queryset)
            if user_queryset:
                reg_no = user_queryset[0].reg_no
                print(reg_no)
                user = authenticate(reg_no=reg_no,password=password)


        if user is not None and user.is_active:
            login(request, user)
            return redirect('booking:home')

        return render(request, self.template_name, {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            reg_no = request.user.reg_no
            password = request.user.password
            user = authenticate(reg_no=reg_no, password=password)
            login(request, user)
        return redirect('booking:home')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'booking/change_password.html', {
        'form': form
    })


def logoutuser(request):
    logout(request)

    return redirect('booking:login')
