# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django import template
from django.db import models

from django.core.urlresolvers import reverse

# 3º libs
import misaka

User = get_user_model()
register = template.Library()
# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(max_length=None, blank=True, default='')
    description_html = models.TextField(max_length=None, editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_groups')

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return self.user.username

