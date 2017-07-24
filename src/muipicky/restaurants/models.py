from django.db import models

# Create your models here.

# created model and added an app therefore need to add to installed apps (in base.py)
class RestaurantLocation(models.Model): 
    # models.Models is the class it's inheriting from so we can map whatever we type here to the db so we can save in the db
    name            = models.CharField(max_length=120)
    location        = models.CharField(max_length=120, null=True, blank=True)
    category        = models.CharField(max_length=120, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    # having auto_now to False means you can change the time and date in the admin. 
    updated         = models.DateTimeField(auto_now=True)
    # my_date_field   = models.DateField(auto_now=False, auto_now_add=False) 