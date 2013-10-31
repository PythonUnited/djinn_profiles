from django.conf.urls.defaults import patterns, url, include
from djinn_contenttypes.views.utils import generate_model_urls
from djinn_profiles.models.userprofile import UserProfile


urlpatterns = patterns('',
    (r'^profiles/', include(generate_model_urls(
                UserProfile,
                name=("djinn_profiles", "userprofile")))),
)
