from django import forms


class RecipeCreationForm(forms.Form):
    name = forms.CharField(max_length=150)
    picture = forms.ImageField()
    prep_time = forms.IntegerField()
    description = forms.CharField(max_length=1500, widget=forms.Textarea)
