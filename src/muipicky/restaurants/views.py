from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# function based view
def home(request):
    #f strings are cool way to do substitutions!
    html_var = 'f strings'
    html_ = f"""
    <!DOCTYPE html>
    <html lang=en>
    <head>
    </head>
    <body>
    <h1>Hello World!</h1>
    <p> This is {html_var} coming through </p>
    </body>
    </html>
    """

    
    return HttpResponse(html_)
    #because it's a function based view it needs to return some sort of response
    
    #return render(request, "home.html", {}) #response