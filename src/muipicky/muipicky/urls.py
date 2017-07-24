"""muipicky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from restaurants.views import ContactView, HomeView, AboutView
# function based views are lowercase and class based are uppercase

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    url(r'^about/$', TemplateView.as_view(template_name = 'about.html')),
    url(r'^contact/(?P<id>\d+)/$', TemplateView.as_view(template_name = 'contact.html')),
]

# because using class view need to create an instance of this class 
    # therefore use .as_view() which makes it run like the function view (a callable base view. )
    # change reg exp slightly to have ability to pass in eg. an id and allowing for
    # some sort of argument to come in