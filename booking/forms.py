from django import forms
from django.utils import timezone
import datetime,calendar
from .models import Book, Confirmation
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib import messages

User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'username', 'reg_no','gender', 'phone_no', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'First Name'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'Second Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'Username'}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'Registration Number'}),
            'gender': forms.Select(attrs={'class': 'form-control pt-0 mt-0', 'placeholder': 'Gender'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control pt-0 mt-0','placeholder': 'Phone'}),
        }
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.isalpha() == False:
            raise forms.ValidationError("Name cant have Numbers")
        else:
            return first_name

    def clean_second_name(self):
        second_name = self.cleaned_data['second_name']

        if second_name.isalpha() == False:
            raise ValidationError('Name cant have numbers')
        else:
            return second_name

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError("Password cant be less than 8 characters")
        elif password.isdigit() == True:
            raise forms.ValidationError("password cant be digits only")
        elif password.isalpha() == True:
            raise forms.ValidationError("password cant be only alphabets")
        else:
            return password


    def clean_reg_no(self):
        reg_no = self.cleaned_data['reg_no']
        slash = 0
        for i in reg_no:
            if i =='/':
                slash+=1
        if reg_no[0] =='/':
            raise forms.ValidationError("Registration number must be in form of S13/1..../16")
        if reg_no[1] =='/':
            raise forms.ValidationError("Registration number must be in form of S13/1..../16")

        if slash != 2:
            raise forms.ValidationError("Registration number must be in form of S13/1..../16")
        else:
            return reg_no

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "Password does not match")
        return cleaned_data

    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']

        if len(phone_no) < 10:
            raise forms.ValidationError("Phone number must be 10 digits")
        if phone_no.isdigit() == False:
            raise forms.ValidationError("Phone number must be only numbers")

        return phone_no

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserUpdate(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'username', 'reg_no', 'phone_no']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']

        if len(phone_no) < 10:
            raise forms.ValidationError("Phone number must be 10 digits")
        if phone_no.isdigit() == False:
            raise forms.ValidationError("Phone number must be only numbers")

        return phone_no



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['reg_no', 'password']
        widgets = {
            'reg_no': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['counsellor1', 'date', 'time']
        widgets = {
            'counsellor1': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%m/%d/%y',
                                    attrs={'class': 'form-control', 'placeholder': 'select a date', 'type': 'date'})
        }


    def clean_time(self):

        date = self.cleaned_data['date']
        if date.weekday() >4:
            print("error shown")
            raise forms.ValidationError("Please you cannot have a session during the weekend")
        time = self.cleaned_data['time']
        date_time = datetime.datetime.combine(date, time)
        if date_time < datetime.datetime.now():
            print('the time is passed')
            raise forms.ValidationError("the time is passed")

        return time


class BookForm1(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['counsellor1', 'date', 'time', 'username']
        widgets = {
            'counsellor1': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%y/%m/%d',
                                    attrs={'class': 'form-control', 'placeholder': 'select a date', 'type': 'date'}),
            'username': forms.Select(attrs={'class': 'form-control'}),
        }

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     students = User.Objects.filter(groups__name="counsellor")
    #     print(username)
    #     print(students)
    #
    #     for reg in students:
    #         if username == reg.username:
    #
    #             print(reg.reg_no)
    #             return reg.reg_no
    #         else:
    #             print(username)
    #             print(reg.reg_no)
    #             raise forms.ValidationError('user not available')



    def clean_time(self):
        date = self.cleaned_data['date']
        if date.weekday() >4:
            print("error shown")
            raise forms.ValidationError("Please you cannot have a session during the weekend")
        time = self.cleaned_data['time']
        date_time = datetime.datetime.combine(date, time)
        if date_time < datetime.datetime.now():
            raise forms.ValidationError("the time is passed")

        return time


class ConfirmationForm(forms.ModelForm):
    class Meta:
        model = Confirmation
        fields = ['counsellor1', 'date', 'time', 'username']

        widgets = {
            'counsellor1': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'date': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'select a date', 'type': 'date', 'readonly': True}),
            'username': forms.Select(attrs={'class': 'form-control',}),
        }

    def clean_time(self):
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        date_time = datetime.datetime.combine(date, time)
        if date_time > datetime.datetime.now():
            raise forms.ValidationError("You can never confirm for the future")
        return time
