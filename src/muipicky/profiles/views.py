from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from menus.models import Item
from restaurants.models import RestaurantLocation

User = get_user_model()

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
        # updating the context data using super, and using args and kwargs as safe guards for context data
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        # print(context)
        user = context['user']
        query = self.request.GET.get('q')
        item_exists = Item.objects.filter(user=user).exists()
        # context location will be equal to the restaurants we already have
        # get_object (method above) because its related to the actual user model itself.
        qs = RestaurantLocation.objects.filter(owner=user).search(query) # with the .search(query) we dont need this if condition (below)
        # if query:
        #     qs = qs.search(query)  # created this .search(query) so we can have a more complex lookup. 
            # this is its own new custom query set as far as the filter is concerned... but not good to have all of that logic there as 
            # you might want to use it again somewhere else.. therefore can put it into models, inside a model manager.
            # if you just use "qs = RestaurantLocation.objects.search(query)" then the user is no longer being passed at all, so it will give you
            # the results of all users who chose that particular restaurant!

        if item_exists and qs.exists(): 
            context['locations'] = qs
        return context