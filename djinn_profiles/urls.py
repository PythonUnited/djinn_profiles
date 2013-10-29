from django.conf.urls.defaults import patterns, url, include
from djinn_contenttypes.views.utils import generate_model_urls
from utils import get_userprofile_model


urlpatterns = patterns('',
    (r'^profiles/', include(generate_model_urls(
                get_userprofile_model(),
                name=("djinn_profiles", "userprofile")))),
)
