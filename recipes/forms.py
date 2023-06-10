from django import forms
from jsonschema.exceptions import ValidationError

from .models import Recipe, Ingredient, Instruction


class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': '100', 'rows': '5'}))

    class Meta:
        model = Recipe
        fields = ['title', 'author', 'category', 'description', 'ingredients', 'instructions']



class IngredientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input'}))
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input'}))

    class Meta:
        model = Ingredient
        fields = ['name', 'quantity']


class InstructionForm(forms.ModelForm):
    step = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-input'}))

    class Meta:
        model = Instruction
        fields = ['step']

