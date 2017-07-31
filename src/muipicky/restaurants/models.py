from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from .utils import unique_slug_generator
from .validators import validate_category 

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.query.QuerySet):
    def search(self, query):
        # this queries down any queryset (filters any queryset?)
        #  RestaurantLocation.objects.all().search(query) or RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip() # gets rid of any spaces
            return self.filter(    # now can do Q lookups and have multiple things here (can search using a variety of contents)
                    Q(name__icontains=query)|
                    Q(location__icontains=query)| 
                    Q(category__icontains=query)| 
                    Q(item__name__icontains=query)|     #  restaurant items/items related to the query set
                    Q(item__contents__icontains=query)
                    ).distinct()
                    # distinct means that on ANY queryset, it will not show it multiple times
        return self  # i.e return nothing

class RestaurantLocationManager(models.Manager):
# you need to put the search logic from views.py for users into a managers function here for it to work.
    def get_queryset(self):
        # need to overide the standard query set
        return RestaurantLocationQuerySet(self.model, using=self._db) # self._db using the same database

    def search(self, query): # this just adds the '.search()' functionality to it. RestaurantLocation.objects.search()
        return self.get_queryset().search(query)
# since we created this manager, need to append to object manager (add to models.objects.all)

class RestaurantLocation(models.Model): 
    owner           = models.ForeignKey(User)
    name            = models.CharField(max_length=120)
    location        = models.CharField(max_length=120, null=True, blank=True)
    category        = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category]) 
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    # my_date_field   = models.DateField(auto_now=False, auto_now_add=False) 
    slug            = models.SlugField(null=True, blank=True)

    objects = RestaurantLocationManager() # adding to Model.objects.all()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return f"/restaurants/{self.slug}"
        return reverse('restaurants:detail', kwargs={'slug': self.slug})
        # have to use restaurant:detail because we've put the restaurant app into a different urls.py file 
        # therefore restaurants is now a namespace and detail is the name itself
        # kwargs = key word arguments. slug = key and self.slug = argument
    @property
    def title(self):
        return self.name # this allows us to write obj.title (as we have defined it as name ) 
    
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        # dont need to call instance.save() because its about to be saved

# def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
#     print('saved')
#     print(instance.timestamp)
#     # instance.save() cannot be used by itself here as we would run into an infinite loop!
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#         instance.save()
        # can save here because we are setting a slug.. and once its created this condition will be false and wont save again.
pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
# post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)