
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
# now its class based view!

class HomeView(TemplateView):
    template_name = 'home.html'
    # need to add overriding context method in TemplateView (a predefined method that comes with this class)
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        # using super to call the default context method on HomeView
        # pass in args and kwargs as a fail safe
        num = None
        some_list = [
            random.randint(0, 10000000),
            random.randint(0, 10000000),
            random.randint(0, 10000000)
        ]
        condition_bool_item = False
        if condition_bool_item:
            num = random.randint(0, 10000000)
        context = {
            "num": num, 
            "some_list": some_list
        }
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

    # because these are just plain template views with not context then we can remove these in the view and 
    # add them to the urls directly!
