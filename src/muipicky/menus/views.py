from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView

from .forms import ItemForm
from .models import Item

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, "home.html", {})
        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = Item.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:3]  # getting all the items related to whether or not i'm following them
        # all the user profiles we are following
        # our users feed
        return render(request, "menus/home-feed.html", {'object_list': qs})
class ItemListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    login_url = '/login/'
    form_class = ItemForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        #these are the arguments we are going to pass into our form class. So in form.py we have to 
        # handle those arguments. 
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create Item'
        return context 

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'menus/detail-update.html'
    form_class = ItemForm
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Item'
        return context 

    def get_form_kwargs(self):
        #if we don't have this then the restaurant list will be empty
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)