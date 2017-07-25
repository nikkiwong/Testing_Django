from django.db.models import Q
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import RestaurantCreateForm
from .models import RestaurantLocation

# functional based view
def restaurant_listview(request):
    template_name = 'restaurants/restaurants_lists.html'
    queryset = RestaurantLocation.objects.all()
    context = {
        "object_list": queryset
    } 
    return render(request, template_name, context)

def restaurant_createview(request):
    form = RestaurantCreateForm(request.POST or None)
    errors = None
    # errors is equal to None because we have to define it before we put it into context

    if form.is_valid():
        obj = RestaurantLocation.objects.create(
            name = form.cleaned_data.get('name'),
            location = form.cleaned_data.get('location'),
            category = form.cleaned_data.get('category')
        )
        return HttpResponseRedirect("/restaurants/")    
    if form.errors:
        errors = form.errors

    template_name = 'restaurants/form.html'
    context = {"form": form, "errors": errors} 
    return render(request, template_name, context)

# class based view
class RestaurantListView(ListView):
     def get_queryset(self):
        slug = self.kwargs.get("slug")
        # can use the .get because it is a dictionary itself
        if slug:
            # use Q lookup for search because want it to be more dynamic and filter either one
            queryset = RestaurantLocation.objects.filter(
                Q(category__iexact=slug) |
                Q(category__icontains=slug)
            )
        else:
            queryset = RestaurantLocation.objects.all()

        return queryset

class RestaurantDetailView(DetailView):
    queryset = RestaurantLocation.objects.all() 

    # def get_object(self, *args, **kwargs):
    #     rest_id = self.kwargs.get('rest_id')
    #     obj = get_object_or_404(RestaurantLocation, id=rest_id) # pk = rest_id
    #     return obj 

 