from django import forms

from .models import Ingredient


class RecipeCreationForm(forms.Form):
    name = forms.CharField(max_length=150)
    picture = forms.ImageField()
    tag = forms.MultipleChoiceField(choices=('L', 'B', 'D'))
    prep_time = forms.IntegerField()
    description = forms.CharField(max_length=1500, widget=forms.Textarea)
    ingredient = forms.ModelChoiceField(Ingredient.objects.all())
    qnt = forms.IntegerField()
