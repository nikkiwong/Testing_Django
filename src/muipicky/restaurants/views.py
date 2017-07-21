import random
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# function based view
   
def home(request):
    num = 0
    some_list = [
        random.randint(0, 10000000),
        random.randint(0, 10000000),
        random.randint(0, 10000000)
    ]
    condition_bool_item = True
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

  
def home2(request):
    context = {
    }
    return render(request, "home2.html", context) 



def home3(request):
    context = {

    }
    return render(request, "home3.html", context) 
