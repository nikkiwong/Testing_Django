from django.conf.urls import url

from .views import ProfileDetailView

urlpatterns = [
    # need to have a look up. in this case we are going to use username, could be used as a slug 
    # depending on how you design your usernames
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='detail'),
]