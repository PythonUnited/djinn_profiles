from itertools import chain
import logging
from activemanager import ActiveManager
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.aggregates import Max
from django.utils.translation import ugettext_lazy as _
from pgauth.models import UserGroup
from django.template.defaultfilters import slugify
from djinn_contenttypes.registry import CTRegistry
from profilebase import ProfileBase
from pgauth.settings import MEMBER_ROLE_ID, INVITED_ROLE_ID, VIEWER_ROLE_ID
from pgauth.models import Role


class AbstractGroupProfile(models.Models):

    name = models.CharField(_('Name'), max_length=100)
    usergroup = models.ForeignKey(UserGroup)


    def set_owner(self, owner):

        """ Override set_owner so as to also make the owner a member
        of the group """

        super(GroupProfile, self).set_owner(owner)
        
        self.usergroup.add_member(owner)

    def _reset_cache(self):
        self.usergroup.cache_is_dirty = True
        self.usergroup.profile

    def members(self):

        """ Return a list of profiles """
        users = self.usergroup.members.all()

        profiles = []
        for user in users:
            try:
                profiles.append(user.get_profile())
            except:
                pass

        def sort_by_profile_name(profile):
            return str(profile)

        profiles = sorted(profiles, key=sort_by_profile_name)

        return profiles

    def is_member(self, user):

        """ Is the given user member of this group?"""
        
        if user == self.get_owner():
            return True

        return user in self.usergroup.members.all()

    def join(self, user):

        """ Add user as member of this group. Handle setting of
        role. Return True if succeeded, else False."""

        if self.is_member(user):
            return False

        self.usergroup.add_member(user)

        # Remove invitee role, if need be
        invitee_role = Role.objects.get(name=INVITED_ROLE_ID)

        self.rm_local_role(invitee_role, user)

        self._reset_cache()
        return True

    def leave(self, user):

        """ Remove user as member of this group. Handle setting of
        role. Return True if succeeded, else False."""

        if not self.is_member(user):
            return False

        member_role = Role.objects.get(name=MEMBER_ROLE_ID)

        self.rm_local_role(member_role, user)

        self.usergroup.members.remove(user)

        self._reset_cache()
        return True

    def invite(self, user_or_group):

        """ Invite the user. Sets the invited role locally. If no luck,
        return False, else True."""

        if not self.is_open_for_invitees:
            return False

        role = Role.objects.get(name=INVITED_ROLE_ID)
        self.add_local_role(role, user_or_group)

        return True

    def get_invitees(self):

        """ Return list of invited users"""

        role = Role.objects.get(name=INVITED_ROLE_ID)

        return self.get_users_for_role(role)

    @property
    def acquire_global_roles(self):

        return False

    def get_local_roles(self, **kwargs):

        """ Override get_local_roles, so as to be able to add invitee """

        roles = super(GroupProfile, self).get_local_roles(**kwargs)

        if self.is_open and kwargs.get('as_role', False):

            invitee = Role.objects.filter(name=INVITED_ROLE_ID).select_related()

            roles = roles | invitee

        # Everyone can see the group
        if kwargs.get('as_role', False):

            viewer = Role.objects.filter(name=VIEWER_ROLE_ID)
            roles = roles | viewer

        return roles

    def save(self, *args, **kwargs):

        super(GroupProfile, self).save(*args, **kwargs)
        self._reset_cache()


    class Meta:

        app_label = 'djinn_profiles'
        verbose_name = _('GroupProfile')
        verbose_name_plural = _('GroupProfiles')
        abstract = True


class GroupProfile(AbstractGroupProfile):

    class Meta:
        app_label = 'djinn_profiles'
        swappable = "GROUPPROFILE_MODEL"


CTRegistry.register("groupprofile", {"class": GroupProfile,
                                     "app": "djinn_profiles",
                                     "label": _("Group"),
                                     "filter_label": _("Groups"),
                                     "name_plural": _("groupprofiles")})
