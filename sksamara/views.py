#coding=utf8
from accounts.models import Person, Company
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import ModelForm
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template.context import RequestContext
from html_mailer import send_mail
from sksamara.models import StaticPage, ConnectionRequest, ConnectionRequestFile, get_site_settings


def context(request):
    return {'pages': StaticPage.objects.filter(publish=True)}


def page(request, slug='index'):

    p = get_object_or_404(StaticPage, slug=slug, publish=True)

    return render_to_response(
        'page.html',
        {'page': p},
        context_instance=RequestContext(request))


@login_required
def client(request):

    user = request.user
    try:
        info = Person.objects.get(id=user.id).info
    except Person.DoesNotExist:
        try:
            info = Company.objects.get(id=user.id).info
        except Company.DoesNotExist:
            info = None

    return render_to_response(
        'info.html',
        {'info': info},
        context_instance=RequestContext(request))


class ConnectionRequestForm(ModelForm):
    class Meta:
        model = ConnectionRequest


class FileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput({'class': 'attachInput'}), required=False)
FileFormSet = formset_factory(FileForm, extra=5)


def connection_request(request):

    form = ConnectionRequestForm(request.POST or None)
    files_formset = FileFormSet(request.POST or None)

    if form.is_valid() and files_formset.is_valid():
        connect_request = form.save()
        for i in range(5):
            key = u'form-%s-file' % i
            if request.FILES.has_key(key):
                file = ConnectionRequestFile(request=connect_request)
                file.file.save(request.FILES[key].name, request.FILES[key])
                file.save()

        emails = get_site_settings().recipients.split(' ')
        link = reverse('admin:%s_%s_change' % (connect_request._meta.app_label, connect_request._meta.module_name),
                       args=[connect_request.id])

        text = u'<a href="http://%s%s">Редактировать<a/>' % (request.get_host(), link)
        send_mail(u'На сайте ООО "Сетевая компания" заполнили заявку на технолонгическое присоединение',
                  {'html': text, 'text': text},
                  settings.EMAIL_FROM,
                  emails)

        return redirect("connection-request-success")

    return render_to_response('connection_request.html', {'form': form,
                                                          'files': files_formset},
                              context_instance=RequestContext(request))


def connection_request_success(request):
    return render_to_response('connection_request_success.html', {}, context_instance=RequestContext(request))



