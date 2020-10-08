import datetime

from .validators import validate_date, validate_time
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django_userforeignkey.models.fields import UserForeignKey


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, second_name,username,reg_no, phone_no,gender, password=None, is_active=True, is_admin=False,
                    is_staff=False):
        if not first_name:
            raise ValueError("User must have a first name")
        if not second_name:
            raise ValueError("User must have a second name")
        if not username:
            raise ValueError("User must have a username")
        if not reg_no:
            raise ValueError("User must have a reg no")
        if not phone_no:
            raise ValueError("User must have phone no")
        if not password:
            raise ValueError("User must specify password")
        user_obj = self.model(
            first_name=first_name,
            second_name=second_name,
            username = username,
            reg_no=reg_no,
            phone_no=phone_no,
            gender =gender,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staff(self, first_name, second_name,username,reg_no, phone_no,gender, password=None):
        user = self.create_user(
            first_name,
            second_name,
            username,
            reg_no,
            phone_no,
            gender,
            password=password,
            is_staff=True
        )

        return user

    def create_superuser(self, first_name, second_name,username,reg_no, phone_no,gender, password=None):
        user = self.create_user(
            first_name,
            second_name,
            username,
            reg_no,
            phone_no,
            gender,


            password=password,
            is_admin=True,
            is_staff=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    gender_choices =(
        ("Male",'Male'),
        ('Female','Female'),
    )
    first_name = models.CharField(max_length=255, default=None)
    second_name = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=20,default=None,unique=True,help_text="choose a unique username")
    reg_no = models.CharField(max_length=255, unique=True,help_text='should be in form of e.g S11/15333/18',null =True,default=None)
    phone_no = models.CharField(max_length=10, unique=True,help_text='must be 10 digits')
    gender = models.CharField(choices=gender_choices,max_length=10,null=True,default=None)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)


    USERNAME_FIELD = 'reg_no'
    REQUIRED_FIELDS = ['first_name', 'second_name','username','phone_no','gender']
    Objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin
    def get_absolute_url(self):
        return reverse('booking:user-details', kwargs={'pk': self.pk})

class Profiles(models.Model):
    user = models.OneToOneField(User, limit_choices_to={'groups__name': "counsellor"},
                                related_name='counsellor_profile_set', on_delete=models.CASCADE, default=None)
    image = models.ImageField()

    def __str__(self):
        return str(self.user.first_name)


class Book(models.Model):
    time_choice = (
        (datetime.time(8, 0), '8-9 AM'),
        (datetime.time(9, 0), '9-10 AM'),
        (datetime.time(10, 0), '10-11 AM'),
        (datetime.time(11, 0), '11-12 PM'),
        (datetime.time(12, 0), '12-1 PM'),
        (datetime.time(13, 0), '1-2 PM'),
        (datetime.time(14, 0), '2-3 PM'),
        (datetime.time(15, 0), '3-4 PM'),
    )
    counsellor1 = models.ForeignKey(User, limit_choices_to={'groups__name': "counsellor"},
                                    related_name='counsellor_set', on_delete=models.CASCADE, default=None)
    time = models.TimeField(choices=time_choice,help_text="choose a time in the future")
    date = models.DateField(help_text='The date must be future or current but time not passed')
    username = models.ForeignKey(User,limit_choices_to={'groups__name': "normal"}, related_name="username_set", on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('booking:home', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.username)


class Confirmation(models.Model):
    counsellor1 = models.ForeignKey(User, limit_choices_to={'groups__name': "counsellor"},
                                    related_name='counsellors', on_delete=models.CASCADE, default=None)
    time = models.TimeField()
    date = models.DateField()
    username = models.ForeignKey(User,limit_choices_to={'groups__name': "normal"}, related_name="usernames", on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('booking:home', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.username.first_name)
