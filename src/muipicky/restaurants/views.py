from django.db.models import Q
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
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
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():
            # need to turn the form into a potential instance, or instance thats going to happen but haven't saved yet
            instance = form.save(commit=False)
            # can customize here
            # pre_save
            instance.owner = request.user
            instance.save()
            # post_save
            return HttpResponseRedirect("/restaurants/")    
        else:
            return HttpResponseRedirect("/login/")
        # not the best practice!
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

class RestaurantCreateView(CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/form.html'
    success_url = "/restaurants/"