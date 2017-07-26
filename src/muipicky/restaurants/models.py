from django.conf import settings

from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator
from .validators import validate_category

User = settings.AUTH_USER_MODEL
# this is a fail safe way to do a customized user model 

# Create your models here.

# created model and added an app therefore need to add to installed apps (in base.py)
class RestaurantLocation(models.Model): 
    # models.Models is the class it's inheriting from so we can map whatever we type here to the db so we can save in the db
    owner           = models.ForeignKey(User) # to get that object, need to use class_instance.model_set.all() 
    name            = models.CharField(max_length=120)
    location        = models.CharField(max_length=120, null=True, blank=True)
    category        = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category]) 
    timestamp       = models.DateTimeField(auto_now_add=True)
    # having auto_now to False means you can change the time and date in the admin. 
    updated         = models.DateTimeField(auto_now=True)
    # my_date_field   = models.DateField(auto_now=False, auto_now_add=False) 

    slug            = models.SlugField(null=True, blank=True)

    # have to implement str method that allows us to return string instead of object
    def __str__(self):
        return self.name

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