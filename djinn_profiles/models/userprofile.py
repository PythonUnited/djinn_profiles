from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from djinn_contenttypes.registry import CTRegistry


class UserProfileManager(models.Manager):

    """
    The manager for the userprofile
    """
    
    def get_by_natural_key(self, name):
        return self.get(name=name)


class AbstractUserProfile(models.Model):

    """ Profile per user """

    name = models.CharField(_('Name'), max_length=100)
    user = models.ForeignKey(User)
    email = models.EmailField(max_length=100, null=True, blank=True)

    objects = UserProfileManager()

    def __unicode__(self):

        return self.name

    def get_owner(self):

        """ Override owner so as to return the user for this profile """

        return self.user

    class Meta:

        app_label = 'djinn_profiles'
        verbose_name = _('UserProfile')
        verbose_name_plural = _('UserProfiles')
        abstract = True


class UserProfile(AbstractUserProfile):

    class Meta:
        app_label = 'djinn_profiles'
        swappable = "DJINN_USERPROFILE_MODEL"


CTRegistry.register("userprofile", {"class": UserProfile,
                                    "app": "djinn_profiles",
                                    "global_add": False,
                                    "filter_label": _("Userprofiles"),
                                    "name_plural": _("Userprofiles")})
