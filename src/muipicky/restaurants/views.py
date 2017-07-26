from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation

def restaurant_listview(request):
    template_name = 'restaurants/restaurants_lists.html'
    queryset = RestaurantLocation.objects.all()
    context = {
        "object_list": queryset
    } 
    return render(request, template_name, context)

@login_required(login_url='/login/')
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

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    login_url = '/login/'
    template_name = 'restaurants/form.html'
    success_url = "/restaurants/"

    def form_valid(self, form):
        instance = form.save(commit=False)
        # making instance from form itself because its a createview so it HAS to be a model form, 
        # not just a regular form. 
        instance.owner = self.request.user
        # the request does come through on every single class based view, 
        # but instead of being passed into individual functions we need to 
        # do self.request!

        # instance.save() <-- don't need this because by default CreateView runs a 
        # form valid method, and at the end of that method, it does that save (in the line below 
        # where you are returning the super). 
        return super(RestaurantCreateView, self).form_valid(form)