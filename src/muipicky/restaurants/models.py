from django.conf import settings

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from .utils import unique_slug_generator
from .validators import validate_category 

User = settings.AUTH_USER_MODEL

class RestaurantLocation(models.Model): 
    owner           = models.ForeignKey(User)
    name            = models.CharField(max_length=120)
    location        = models.CharField(max_length=120, null=True, blank=True)
    category        = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category]) 
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    # my_date_field   = models.DateField(auto_now=False, auto_now_add=False) 
    slug            = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return f"/restaurants/{self.slug}"
        return reverse('restaurant-detail', kwargs={'slug': self.slug})
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