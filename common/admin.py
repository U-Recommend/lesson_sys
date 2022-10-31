from django.contrib import admin

admin.site.site_title = "Python课程系统"
admin.site.site_header = "Python课程系统"

from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from common.models import User


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)


class MyUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)


class MyUserAdmin(UserAdmin):
    list_display = ("name", "username", "is_active")
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ("name",)
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    filter_horizontal = ()
    sortable_by = ""
    exclude = ('user_permissions', 'first_name', 'groups', 'email', 'last_name')

    def changelist_view(self, request, extra_context=None):
        user = request.user
        if user.is_superuser:
            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
                              (_('Personal info'), {'fields': ('name',)}),
                              (_('Permissions'), {'fields': ('is_active', 'is_superuser')}),
                              (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                              )
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': ('username', 'name', 'password1', 'password2', 'is_active',
                                                     'is_superuser'),
                                          }),
                                  )
        return super(MyUserAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        obj.is_staff = 1
        user = request.user
        if user.is_anonymous:
            return
        super().save_model(request, obj, form, change)
        if not change:
            obj.is_active = 1
            obj.save()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.register(User, MyUserAdmin)
