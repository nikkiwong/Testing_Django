
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
# function based view
   
def home(request):
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
    return render(request, "home.html", context) #response
#{} is a python dictionary.
# Django uses logic that goes with the templates
# it takes in request, some template, extra context and produces results.  

  
def about(request):
    context = {
    }
    return render(request, "about.html", context) 

def contact(request):
    context = {
    }
    return render(request, "contact.html", context) 

class ContactView(View):
    # need to define what kind of method this view is allows for (eg 'GET'/'POST')
    def get(self, request, *args, **kwargs):
        # because its a method inside of a class you need to have 'self' as a parameter
        # get method is a type of request (getting info from the server)
        context = {}
        return render(request, "contact.html", context) 
