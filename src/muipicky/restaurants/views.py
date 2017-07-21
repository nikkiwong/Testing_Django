import random
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# function based view

# def home_old(request):
#     # f strings are cool way to do substitutions! you need the f before the comment
#     # and the {} where you want to sub
#     html_var = 'f strings'
#     html_ = f"""
#     <!DOCTYPE html>
#     <html lang=en>
#     <head>
#     </head>
#     <body>
#     <h1>Hello World!</h1>
#     <p> This is {html_var} coming through </p>
#     </body>
#     </html>
#     """
       
#     return HttpResponse(html_)
#     #because it's a function based view it needs to return some sort of response
    
def home(request):
    num = random.randint(0, 10000000)
    some_list = [num, random.randint(0, 10000000), random.randint(0, 10000000)]
    context = {
        "bool_item": False,
        "num": num, 
        "some_list": some_list
    }
    return render(request, "base.html", context) #response
#{} is a python dictionary.
# Django uses logic that goes with the templates
# it takes in request, some template, extra context and produces results.  