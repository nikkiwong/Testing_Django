import random
from django.http import HttpResponse
from django.shortcuts import render

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
