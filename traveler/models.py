#coding=utf8
#from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Person(AbstractUser):
    city_from = models.CharField(verbose_name=u'Город', max_length=200,
                                 blank=True, null=True)
    country = models.CharField(verbose_name=u'Страна', max_length=100,
                                 blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=100,
                             blank=True, null=True)
    text = models.TextField(verbose_name=u'О себе', null=True, blank=True)
    vk_id = models.CharField(verbose_name=u'VK ID', max_length=200,
                             blank=True, null=True)
    cities_add = models.ManyToManyField(to='City', blank=True)
    # persons_add = models.ManyToManyField(to='self', blank=True)
    likes = GenericRelation('Like')
    tags = GenericRelation('Tag')
    # image = models.ImageField(verbose_name=u'Аватар', blank=True, null=True)

    class Meta:
        ordering = ['date_joined']
        verbose_name = u'Человек'
        verbose_name_plural = u'Люди'

    def __unicode__(self):
        return self.get_full_name()


class Message(models.Model):
    from_person = models.ForeignKey(to=Person, related_name='from_message')
    to_person = models.ForeignKey(to=Person, related_name='whom_message')
    text = models.TextField(verbose_name=u'Текст')
    time = models.DateTimeField(verbose_name=u'Время отправления',
                                auto_now_add=True)

    read_flag = models.BooleanField(verbose_name=u'Флаг прочтения', default=False)

    class Meta:
        ordering = ['time']
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'

    def __unicode__(self):
        return self.from_person.last_name + ' -> ' + self.to_person.last_name


class Comment(models.Model):
    text = models.TextField(verbose_name=u'Текст')
    person = models.ForeignKey(to=Person)
    city = models.ForeignKey(to='City', blank=True, null=True)
    time = models.DateTimeField(verbose_name=u'Время отправления')
    comment_id = models.ForeignKey(to='self', blank=True, null=True)

    class Meta:
        ordering = ['-time']
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

    def __unicode__(self):
        return self.person.last_name + ' ' + self.person.first_name


class Country(models.Model):
    name = models.CharField(db_index=True, verbose_name=u'Название', max_length=50)
    description = models.TextField(verbose_name=u'Описание',
                                   blank=True, null=True)
    likes = GenericRelation('Like')
    tags = GenericRelation('Tag')
    likes_count = models.IntegerField(db_index=True, verbose_name=u'Количество лайков',
                                        default=0)
    views_count = models.IntegerField(verbose_name=u'Количество просмотров', default=0)

    class Meta:
        # ordering = ['name']
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(db_index=True, verbose_name=u'Название', max_length=100)
    country = models.ForeignKey(to=Country)
    description = models.TextField(verbose_name=u'Описание',
                                   blank=True, null=True)
    likes_count = models.IntegerField(db_index=True, verbose_name=u'Количество лайков',
                                default=0)
    tags = GenericRelation('Tag')
    views_count = models.IntegerField(verbose_name=u'Количество просмотров', default=0)

    class Meta:
        ordering = ['name']
        verbose_name = u'Город'
        verbose_name_plural = u'Города'

    def __unicode__(self):
        return self.name


class Trip(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    persons = models.ManyToManyField(to=Person)
    date_start = models.DateField(db_index=True, verbose_name=u'Дата начала')
    date_end = models.DateField(verbose_name=u'Дата окончания')
    city = models.ForeignKey(to=City)
    open_flag = models.BooleanField(verbose_name=u'Флаг записи')
    tags = GenericRelation('Tag')

    class Meta:
        ordering = ['-date_start']
        verbose_name = u'Поездка'
        verbose_name_plural = u'Поездки'

    def __unicode__(self):
        return self.name


class Like(models.Model):
    person = models.ForeignKey(to=Person)
    object_id = models.IntegerField(verbose_name=u'ID объекта')
    content_type = models.ForeignKey(to=ContentType)
    relation = GenericForeignKey('content_type', 'object_id')
    time = models.DateTimeField(verbose_name=u'Время', auto_now_add=True)

    class Meta:
        verbose_name = u'Лайк'
        verbose_name_plural = u'Лайки'
        unique_together = ('person', 'content_type', 'object_id')

    def __unicode__(self):
        return self.person.last_name + ' ' + self.person.first_name



class Tag(models.Model):
    person = models.ForeignKey(to=Person)
    text = models.CharField(db_index=True, verbose_name=u'Текст', max_length=100)
    object_id = models.IntegerField(verbose_name=u'ID объекта')
    content_type = models.ForeignKey(to=ContentType)
    relation = GenericForeignKey('content_type', 'object_id')
    time = models.DateTimeField(verbose_name=u'Время', auto_now_add=True)

    class Meta:
        verbose_name = u'Тег'
        verbose_name_plural = u'Теги'
        index_together = ('object_id', 'content_type')

    def __unicode__(self):
        return self.text
