from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps as django_apps
from .userprofile import UserProfile
from .groupprofile import GroupProfile


def get_groupprofile_model():
    """
    Return the GroupProfile model that is active in this project.
    """
    try:
        return django_apps.get_model(
            settings.DJINN_GROUPPROFILE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "DJINN_GROUPPROFILE_MODEL must be of the form "
            "'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "DJINN_GROUPPROFILE_MODEL refers to model '%s' that has not been "
            "installed" % settings.DJINN_GROUPPROFILE_MODEL
        )


def get_userprofile_model():
    """
    Return the UserProfile model that is active in this project.
    """
    try:
        return django_apps.get_model(
            settings.DJINN_USERPROFILE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "DJINN_USERPROFILE_MODEL must be of the form "
            "'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "DJINN_USERPROFILE_MODEL refers to model '%s' that has not been "
            "installed" % settings.DJINN_USERPROFILE_MODEL
        )
