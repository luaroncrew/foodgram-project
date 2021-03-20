from django import forms

from .models import Recipe


class RecipeCreationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'picture', 'prep_time', 'description']
