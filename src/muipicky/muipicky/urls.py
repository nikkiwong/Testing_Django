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

from restaurants.views import home, about, contact, ContactView
# function based views are lowercase and class based are uppercase

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home),
    url(r'^about/$', about),
    url(r'^contact/(?P<id>\d+)/$', ContactView.as_view()),
]

# because using class view need to create an instance of this class 
    # therefore use .as_view() which makes it run like the function view (a callable base view. )
    # change reg exp slightly to have ability to pass in eg. an id and allowing for
    # some sort of argument to come in