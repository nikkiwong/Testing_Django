
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from .models import RestaurantLocation

# functional based view
def restaurant_listview(request):
    template_name = 'restaurants/restaurants_lists.html'
    queryset = RestaurantLocation.objects.all()
    context = {
        "object_list": queryset
    } 
    return render(request, template_name, context)

# class based view
class RestaurantListView(ListView):
    queryset = RestaurantLocation.objects.all()
    template_name = 'restaurants/restaurants_lists.html'

class MexicanRestaurantListView(ListView):
    queryset = RestaurantLocation.objects.filter(category__iexact='mexican')
    template_name = 'restaurants/restaurants_lists.html'

class AsianFusionRestaurantListView(ListView):
    queryset = RestaurantLocation.objects.filter(category__iexact='asian fusion')
    template_name = 'restaurants/restaurants_lists.html'