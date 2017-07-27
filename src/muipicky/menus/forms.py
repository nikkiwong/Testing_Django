from django import forms

from restaurants.models import RestaurantLocation
#RestaurantLocation is the model (restaurant) we are using (changing queryset for FK here)!

from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'restaurant',
            'name',
            'contents',
            'excludes',
            'public'
        ]

    def __init__(self, user=None, *args, **kwargs):
        # print(kwargs.pop('user'))
        print(user)
        super(ItemForm, self).__init__(*args,**kwargs)
        #all we are doing here is passing in a user now to our item form. 
        self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user)