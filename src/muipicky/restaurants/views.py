from django.db.models import Q
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

class SearchRestaurantListView(ListView):
    template_name = 'restaurants/restaurants_lists.html'

    def get_queryset(self):
        print(self.kwargs)
        slug = self.kwargs.get("slug")
        # can use the .get because it is a dictionary itself
        if slug:
            # use Q lookup for search because want it to be more dynamic and filter either one
            queryset = RestaurantLocation.objects.filter(
                Q(category__iexact=slug) |
                Q(category__icontains=slug)
            )
        else:
            queryset = RestaurantLocation.objects.none()
        return queryset