#coding=utf8
from django import forms
from accounts.models import Person, Company
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin


class CommonAccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        return self.initial["password"]

    class Meta:
        abstract = True


class PersonChangeForm(CommonAccountChangeForm):
    class Meta:
        model = Person

    def __init__(self, *args, **kwargs):
        super(PersonChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True


class CompanyChangeForm(CommonAccountChangeForm):
    class Meta:
        model = Company


    def __init__(self, *args, **kwargs):
        super(CompanyChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class PersonAdmin(UserAdmin):
    form = PersonChangeForm
    list_display = 'email', 'last_name', 'first_name', 'patronymic', 'city', 'address', 'phone', 'date_joined', 'is_active'
    list_filter = 'is_active',
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('email', 'is_active', 'password', 'last_name', 'first_name', 'patronymic', 'city', 'address', 'phone', 'date_joined')
        }),
        (u'Страница пользователя', {
            'fields': ('info',)
        })
    )

admin.site.register(Person, PersonAdmin)


class CompanyAdmin(UserAdmin):
    form = CompanyChangeForm
    list_display = 'email', 'name', 'inn', 'chief_post', 'chief_lastname', 'chief_name', 'chief_lastname', 'address', 'phone', 'date_joined', 'is_active'
    list_filter = 'is_active',
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('email', 'is_active', 'password', 'name', 'inn', 'kpp', 'ogrn', 'chief_name', 'chief_lastname', 'chief_patronymic', 'chief_post', 'chief_basement', 'address', 'phone'
            )
        }),
        (u'Страница пользователя', {
            'fields': ('info',)
        })
    )

admin.site.register(Company, CompanyAdmin)