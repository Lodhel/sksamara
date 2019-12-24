#coding=utf8
from django.core.urlresolvers import reverse
from tinymce import models as tinymce_models
from django.db import models


class StaticPage(models.Model):
    title = models.CharField(u'Пункт меню', max_length=250)
    slug = models.SlugField(u'Url', max_length=250)
    text = tinymce_models.HTMLField(u'Текст страницы')
    publish = models.BooleanField(u'Публиковать', default=True)
    order = models.IntegerField(u'Порядок вывода', default=1)

    class Meta:
        verbose_name = u"Страница"
        verbose_name_plural = u"Страницы сайта"
        ordering = 'order',

    def get_absolute_url(self):
        return reverse('page', args=[str(self.slug)])


class ConnectionRequest(models.Model):
    full_name = models.CharField(u'Фамилия, имя, отчество/Полное название организации', max_length=150)
    name = models.CharField(u'Имя', max_length=150)
    status = models.IntegerField(u'Статус', choices=((1, u'Физическое лицо'), (2, u'Юридическое лицо')))
    area = models.CharField(u'Район Самарской области', max_length=100)
    city = models.CharField(u'Город Самарской области', max_length=100)
    inn = models.CharField(u'Реквизиты СНИЛС/ИНН', max_length=50)
    phone = models.CharField(u'Телефон/факс с указанием кода города', max_length=50)
    email = models.EmailField(u'Электронная почта', max_length=50)
    comment = models.TextField(u'Вопросы и комментарии', null=True, blank=True)
    date = models.DateTimeField(u'Дата и время', auto_now_add=True)

    class Meta:
        verbose_name = u"Заявка"
        verbose_name_plural = u"Заявки на технологическое присоединение"
        ordering = '-date',


class ConnectionRequestFile(models.Model):
    request = models.ForeignKey(ConnectionRequest)
    file = models.FileField(upload_to='connection_request')


class SiteSettings(models.Model):
    recipients = models.CharField(u'Адреса, куда высылать письма', help_text=u'Задавать через пробел', max_length=200)

    class Meta:
        verbose_name = u"настройки"
        verbose_name_plural = u"настройки"

    def __unicode__(self):
        return u'Настройки'


def get_site_settings():
    try:
        return SiteSettings.objects.all()[0]
    except IndexError:
        return SiteSettings.objects.create()
