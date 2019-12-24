# coding:utf-8
from datetime import datetime
import hashlib
import random
from accounts.models import RegistrationConfirm, Person
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from accounts.forms import LoginForm, RegistrationForm, PersonForm, CompanyForm, ResetForm, SmsForm
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from html_mailer import send_mail, mail_admins
from sksamara.models import get_site_settings


def log_in(request):
    form = LoginForm(request.POST or None, initial={'next': request.GET.get('redirect', request.GET.get(REDIRECT_FIELD_NAME, '/'))})
    form.request = request
    if form.is_valid():
        return redirect(form.cleaned_data['next'])

    return render_to_response("accounts/login.html", locals(), RequestContext(request))


def log_out(request):
    auth.logout(request)
    return render_to_response('accounts/logout.html', {}, context_instance=RequestContext(request))


def pre_registration(request):
    return render_to_response('accounts/pre_registration.html', {}, context_instance=RequestContext(request))


def set_pwd_and_mailout(instance, request):

    rc = RegistrationConfirm.objects.create(
        user=instance,
        key=hashlib.sha1(datetime.now().isoformat() + str(random.randrange(1, 100000000000000000000)) + instance.email).hexdigest())

    password = hashlib.sha1(datetime.now().isoformat() + str(random.randrange(1, 100000000000000000000)) + instance.email).hexdigest()
    password = password[:8]

    instance.set_password(password)
    instance.is_active=False
    instance.save()

    context = {'key': rc.key, 'email': rc.user.email, 'password': password}
    send_mail(u'Вы успешно зарегистрированы на сайте ООО "Сетевая компания": ',
              {'html': render_to_string('accounts/email/registration_confirm.html', context),
               'text': render_to_string('accounts/email/registration_confirm.txt', context)},
              settings.EMAIL_FROM,
              [instance.email])

    emails = get_site_settings().recipients.split(' ')
    link = reverse('admin:%s_%s_change' %(instance._meta.app_label,  instance._meta.module_name),  args=[instance.id] )

    text = u'<a href="http://%s%s">Редактировать<a/>' % (request.get_host(), link)
    send_mail(u'На сайте ООО "Сетевая компания" зарегистрировался новый пользователь',
              {'html': text, 'text': text},
              settings.EMAIL_FROM,
              emails)


def person_registration(request):
    form = PersonForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        set_pwd_and_mailout(instance, request)
        return redirect(reverse('registration-complete'))

    return render_to_response("accounts/registration.html", locals(), RequestContext(request))


def company_registration(request):
    form = CompanyForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        set_pwd_and_mailout(instance, request)
        return redirect(reverse('registration-complete'))

    return render_to_response("accounts/registration.html", locals(), RequestContext(request))


def registration_complete(request):
    return render_to_response("accounts/registration_complete.html", locals(), RequestContext(request))


def registration_confirm(request, key):

    rc = get_object_or_404(RegistrationConfirm, key=key)
    rc.user.is_active = True
    rc.user.save()

    return redirect('login')


@csrf_exempt
def reset_password(request):
    form = ResetForm(request.POST or None)
    return render_to_response("accounts/reset_password.html", locals(), RequestContext(request))


def reset_target(request):
    return render_to_response("accounts/reset_target.html", locals(), RequestContext(request))


@csrf_exempt
def send_sms(request):
    form = SmsForm(request.POST or None)
    if form.is_valid():
        instance = form.is_valid()
        user = Person.objects.get(phone=instance.person)
        password = hashlib.sha1(datetime.now().isoformat() + str(random.randrange(1, 100000000000000000000)) + user.email).hexdigest()
        password = password[:8]

        password = instance.set_password(password)

        user.password = password
        user.save()

        return redirect(reverse('registration-complete'))

    return render_to_response("accounts/send_sms.html", locals(), RequestContext(request))
