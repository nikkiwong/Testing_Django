from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View, CreateView

from menus.models import Item
from restaurants.models import RestaurantLocation

from .forms import RegisterForm
from .models import Profile
User = get_user_model()

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'
    # sends them to homepage, because want to send them an email to verify this registration

    def dispatch(self, *args, **kwargs): # override function 
        # if self.request.user.is_authenticated():
        #     return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)

class ProfileFollowToggle(LoginRequiredMixin, View): # endpoint
    def post(self, request, *args, **kwargs):
        # print(request.data)
        # print(request.POST)
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        print(is_following)
        # profile_ = Profile.objects.get(user__username__iexact=user_to_toggle)
        # user = request.user
        # if user in profile_.followers.all(): 
        #     profile_.followers.remove(user)
        # else:
        #     profile_.followers.add(user)
        return redirect(f"/u/{profile_.user.username}/")
    # This logic though SHOULD exist inside the model!!!!


class ProfileDetailView(DetailView):
    # queryset = User.objects.filter(is_active=True)
    # dont neet queryset anymore because using get_object call instead
    template_name = 'profiles/user.html'

    def get_object(self):
        # all we are getting here is the user object and want to return back the user object to any given profile
        username = self.kwargs.get("username")
        if username is None:
            raise Http404   # there most likely is a default 404 exception raised if there are no usernames when 
            # you use dictionary get but this is just a safe guard 
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        item_exists = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user).search(query) 
        if item_exists and qs.exists(): 
            context['locations'] = qs
        return context