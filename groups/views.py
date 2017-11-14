# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Group, GroupMember

# Create your views here.
class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group

class SingleGroupView(generic.DetailView):
    model = Group

class ListGroupsView(generic.ListView):
    model = Group
    context_object_name = 'groups'

class JoinGroupView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'warning already member')
        else:
            messages.success(self.request, 'you are now a member')

        return super(JoinGroupView, self).get(request, *args, **kwargs)


class LeaveGroupView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you aren\t in this group')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group')

        return super(LeaveGroupView, self).get(request, *args, **kwargs)
