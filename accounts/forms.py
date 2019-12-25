# coding:utf-8
import random
import string

from accounts.models import Person, Company, SmsPerson, SmsCompany
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms.models import ModelForm
import requests


class LoginForm(forms.Form):
    email = forms.CharField(label=u'Ваш e-mail')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
    next = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = auth.authenticate(username=email, password=password)

            if user is not None:
                if user.is_active:
                    auth.login(self.request, user)
                else:
                    raise forms.ValidationError(u'Данный пользователь неактивен.')
            else:
                raise forms.ValidationError(u'Неверные имя пользователя или пароль.')
        return self.cleaned_data


class RegistrationForm(forms.Form):

    email = forms.EmailField(label=u'Ваш e-mail')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput())

    def clean(self):
        users = User.objects.filter(email__iexact=self.cleaned_data.get('email', '-1'))
        # if self.unit_id:
        #     users = users.exclude(id=self.unit_id)
        if users.count():
            raise forms.ValidationError(u'К сожалению, данный адрес электронной почты занят другим игроком.')

        p = self.cleaned_data.get('password')
        pc = self.cleaned_data.get('password_confirm')
        if pc != p:
            raise forms.ValidationError(u'Введеные пароли не совпадают.')

        return self.cleaned_data


class PersonForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True

    class Meta:
        model = Person
        fields = ['email', 'last_name', 'first_name', 'patronymic', 'city', 'address', 'phone']

    def clean(self):
        users = User.objects.filter(email__iexact=self.cleaned_data.get('email', '-1'))
        if users.count():
            raise forms.ValidationError(u'К сожалению, данный адрес электронной почты уже занят.')

        self.instance.username = self.cleaned_data.get('email')

        return self.cleaned_data


class CompanyForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = Company
        fields = ['email', 'name', 'inn', 'kpp', 'ogrn', 'chief_lastname', 'chief_name', 'chief_patronymic',
                  'chief_post', 'chief_basement', 'address', 'phone']

    def clean(self):
        users = User.objects.filter(email__iexact=self.cleaned_data.get('email', '-1'))
        if users.count():
            raise forms.ValidationError(u'К сожалению, данный адрес электронной почты уже занят.')

        self.instance.username = self.cleaned_data.get('email')

        return self.cleaned_data


class Gate:

    def __init__(self, login, password):
        self.password = password
        self.login = login

    def send(self, phone, text):
        data = {
            "login": self.login,
            "password": self.password,
            "phone": phone,
            "text": text
        }

        requests.get("http://api.prostor-sms.ru/messages/v2/send/", data)


class ResetForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResetForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['phone'].label = ''

    class Meta:
        model = Person
        fields = ['phone', ]

    def generate(self, size=4, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def clean(self):
        try:
            phone = self.cleaned_data.get('phone')
            sms = self.generate()
            try:
                user = Person.objects.get(phone=phone)
            except:
                user = Person.objects.get(phone="+{}".format(phone))

            sender = Gate('vf141149', '703271')
            sender.send(phone, "Ваш код для изменения пароля: {}".format(sms))

            try:
                person = SmsPerson.objects.get(person=phone)
            except:
                try:
                    person = SmsPerson.objects.get(person="+{}".format(phone))
                except:
                    person = None

            if person:
                person.delete()

            person = SmsPerson(person=phone, sms=sms)
            person.save()
        except:
            raise forms.ValidationError(u'Пользователь не найден')


class SmsForm(ModelForm):

    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SmsForm, self).__init__(*args, **kwargs)
        self.fields['sms'].required = True
        self.fields['person'].required = True
        self.fields['sms'].label = 'код из смс'
        self.fields['person'].label = 'номер телефона'

    class Meta:
        model = SmsPerson
        fields = ['sms', "person"]

    def clean(self):
        if self.cleaned_data["password_confirm"] != self.cleaned_data["password"]:
                raise forms.ValidationError(u'К сожалению, пароли не совпадают.')
        if len(self.cleaned_data["password"]) < 8:
                raise forms.ValidationError(u'Пароль должен быть не менее 8 символов.')
        try:
            sms = self.cleaned_data.get('sms')
            person = self.cleaned_data.get('person')

            try:
                target = SmsPerson.objects.get(person=person)
            except:
                target = SmsPerson.objects.get(person=person)

            if target.sms != sms:
                raise forms.ValidationError(u'К сожалению, код не совпадает.')

            try:
                user = Person.objects.get(phone=person)
            except:
                user = Person.objects.get("+{}".format(person))

        except:
            raise forms.ValidationError(u'Что то пошло не так.')


class CompanyResetForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompanyResetForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['phone'].label = ''

    class Meta:
        model = Company
        fields = ['phone', ]

    def generate(self, size=4, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def clean(self):
        try:
            phone = self.cleaned_data.get('phone')
            sms = self.generate()
            try:
                user = Company.objects.get(phone=phone)
            except:
                user = Company.objects.get(phone="+{}".format(phone))

            sender = Gate('vf141149', '703271')
            sender.send(phone, "Ваш код для изменения пароля: {}".format(sms))

            try:
                person = SmsCompany.objects.get(person=phone)
            except:
                try:
                    person = SmsCompany.objects.get(person="+{}".format(phone))
                except:
                    person = None

            if person:
                person.delete()

            person = SmsCompany(person=phone, sms=sms)
            person.save()
        except:
            raise forms.ValidationError(u'Пользователь не найден')


class CompanySmsForm(ModelForm):

    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(CompanySmsForm, self).__init__(*args, **kwargs)
        self.fields['sms'].required = True
        self.fields['person'].required = True
        self.fields['sms'].label = 'код из смс'
        self.fields['person'].label = 'номер телефона'

    class Meta:
        model = SmsCompany
        fields = ['sms', "person"]

    def clean(self):
        if self.cleaned_data["password_confirm"] != self.cleaned_data["password"]:
                raise forms.ValidationError(u'К сожалению, пароли не совпадают.')
        if len(self.cleaned_data["password"]) < 8:
                raise forms.ValidationError(u'Пароль должен быть не менее 8 символов.')
        try:
            sms = self.cleaned_data.get('sms')
            person = self.cleaned_data.get('person')

            try:
                target = SmsCompany.objects.get(person=person)
            except:
                target = SmsCompany.objects.get(person=person)

            if target.sms != sms:
                raise forms.ValidationError(u'К сожалению, код не совпадает.')

            try:
                user = Company.objects.get(phone=person)
            except:
                user = Company.objects.get("+{}".format(person))

        except:
            raise forms.ValidationError(u'Что то пошло не так.')
