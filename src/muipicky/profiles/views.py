from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

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