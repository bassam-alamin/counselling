from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import Book, Profiles, Confirmation
from django.contrib.auth import get_user_model
from .forms import UserForm

User = get_user_model()


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None,{'fields':('phone_no','password')}),
        ('Personal info',{'fields':('first_name', 'second_name','username')}),
        ('Permissions',{'fields':('active','admin','staff','groups','user_permissions')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('reg_no',)}),
        ('Personal info', {'fields': ('first_name', 'second_name','username','phone_no')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','second_name','username','phone_no','gender','password', 'password_confirm')}
         ),
    )
    model = User
    add_form = UserForm
    list_display = ['first_name','second_name','reg_no']
    list_filter = ['groups']
    search_fields = ['first_name','second_name','reg_no']
    ordering = ['reg_no']

class ConfirmationModelAdmin(admin.ModelAdmin):
    list_display = ["counsellor1", "date", "username"]
    list_filter = ["counsellor1", "time",'username']

    class Meta:
        model = Confirmation

admin.site.register(User,UserAdmin)
admin.site.site_header="Student Counselling Administration"
admin.site.register(Profiles)
admin.site.register(Confirmation,ConfirmationModelAdmin)
