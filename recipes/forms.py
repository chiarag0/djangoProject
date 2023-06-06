from django import forms
from jsonschema.exceptions import ValidationError

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'author', 'category', 'description', 'ingredients', 'instructions']


class IngredientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input'}))
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input'}))

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']

    def __init__(self, *args, **kwargs):
        ingredient_prefix = kwargs.pop('ingredient_prefix')
        super().__init__(*args, **kwargs)
        self.prefix = ingredient_prefix


class InstructionForm(forms.ModelForm):
    step = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input'}))

    class Meta:
        model = Ingredient
        fields = ['step']