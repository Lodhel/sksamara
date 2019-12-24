# coding:utf-8
import random
import string

from accounts.models import Person, Company, SmsPerson
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
            user = Person.objects.get(phone=self.cleaned_data.get('phone'))
            sender = Gate('vf141149', '703271')
            sender.send(phone, "Ваш код для изменения пароля: {}".format(sms))
            person = SmsPerson(person=user, sms=sms)
            person.save()
        except:
            pass


class SmsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SmsForm, self).__init__(*args, **kwargs)
        self.fields['sms'].required = True

    class Meta:
        model = SmsPerson
        fields = ['sms', ]

    def clean(self):
        try:
            sms = self.cleaned_data.get('sms')
            objects = SmsPerson.objects.all()
            print()
        except:
            pass

