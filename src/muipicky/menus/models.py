from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from restaurants.models import RestaurantLocation

class Item(models.Model):
    # association stuff
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    restaurant      = models.ForeignKey(RestaurantLocation)
    # Every item created has to have a user and every item has to have a restaurant too. 
    # real item stuff
    name            = models.CharField(max_length=120)
    contents        = models.TextField(help_text='Separate each item by comma')
    # contents is how you want it
    excludes        = models.TextField(blank=True, null=True, help_text='Separate each item by comma')
    public          = models.BooleanField(default=True)
    # public if you want to share it with everyone in the world
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # return f"/restaurants/{self.slug}"
        return reverse('menus:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-updated', '-timestamp']

    def get_contents(self):
        return self.contents.split(",")

    def get_excludes(self):
        return self.excludes.split(",")