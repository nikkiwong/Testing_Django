from django import forms

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