from django import forms
from .models import RestaurantLocation
from .validators import validate_category

class RestaurantCreateForm(forms.Form):
    name            = forms.CharField()
    location        = forms.CharField(required=False)
    category        = forms.CharField(required=False)

    def clean_name(self):
        # this is a custom way to validate data.
        # this method is called when we validate the form in the views.py
        name = self.cleaned_data.get("name")
        if name == "Hello":
            raise forms.ValidationError("Not a valid name")
        return name

class RestaurantLocationCreateForm(forms.ModelForm):
    # email   = forms.EmailField()
    category  = forms.CharField(required=False, validators=[validate_category])
    # overriding the default for category (validation is on the form itself)
    class Meta:
        model = RestaurantLocation
        fields = [
            'name',
            'location',
            'category'
        ]

    def clean_name(self):
        # this is a custom way to validate data.
        # this method is called when we validate the form in the views.py
        name = self.cleaned_data.get("name")
        if name == "Hello":
            raise forms.ValidationError("Not a valid name")
        return name

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if ".edu" in email:
    #         raise forms.ValidationError("We do not accept .edu email")
    #     return email