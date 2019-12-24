#coding=utf8
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.db import models


class Person(User):
    patronymic = models.CharField(u'Отчество', max_length=100)
    city = models.CharField(u'Населенный пуект', max_length=100)
    address = models.CharField(u'Адрес', max_length=100)
    phone = models.CharField(u'Телефон', max_length=100)
    info = tinymce_models.HTMLField(u'Информация', null=True, blank=True)

    class Meta:
        verbose_name = u"Физ. лицо"
        verbose_name_plural = u"Физ. лица"


class SmsPerson(models.Model):
    person = models.OneToOneField(Person)
    sms = models.CharField(max_length=6)


class Company(User):
    name = models.CharField(u'Наименование организации', max_length=120)
    inn = models.CharField(u'ИНН', max_length=20)
    kpp = models.CharField(u'КПП', max_length=20)
    ogrn = models.CharField(u'ОГРН', max_length=20)
    chief_name = models.CharField(u'Имя руководителя', max_length=50)
    chief_lastname = models.CharField(u'Фамилия руководителя', max_length=50)
    chief_patronymic = models.CharField(u'Отчество руководителя', max_length=50, blank=True, null=True)
    chief_post = models.CharField(u'Должность руковоителя', max_length=50)
    chief_basement = models.IntegerField(u'Основание совершения действия руководителем', choices=((1, u'Устав'), (2, u'Доверенность ')))
    address = models.CharField(u'Адрес', max_length=100)
    phone = models.CharField(u'Телефон', max_length=100)
    info = tinymce_models.HTMLField(u'Информация', null=True, blank=True)

    class Meta:
        verbose_name = u"Юр. лицо"
        verbose_name_plural = u"Юр. лица"


class RegistrationConfirm(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)