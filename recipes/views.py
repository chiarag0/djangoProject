from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from . import models
from .forms import RecipeForm, IngredientForm
from django.contrib.auth.decorators import login_required

from .models import Recipe, Ingredient

""""
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            # Process the form data and save the new recipe
            form.save()
            # Redirect to a success page or display a success message
            return redirect('recipe_list')
    else:
        form = RecipeForm()

    return render(request, 'recipes/create_recipe.html', {'form': form})



def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})
    
    """


# Create your views here.
def home(request):
    recipes = models.Recipe.objects.all()
    context = {
       'recipes': recipes
          }
    return render(request, 'recipes/home.html', context)


class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'


class RecipeDetailView(DetailView):
    model = models.Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.filter(recipe=self.object)
        return context



class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('recipes-home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    fields = ['title', 'author', 'category', 'description']
    template_name = 'recipes/create_recipe_start.html'

    def __init__(self):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.pk
        print(pk)
        return reverse_lazy('ingredients-create', kwargs={'pk': pk})


class IngredientsCreateView(CreateView):

    form_class = IngredientForm
    template_name = 'recipes/create_recipe_ingredients.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['ingredient_prefix'] = 'ingredient'  # Imposta un prefisso univoco per ogni ingrediente
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = models.Recipe.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        recipe_pk = self.kwargs['pk']
        recipe = Recipe.objects.get(pk=recipe_pk)

        # Salva tutti gli ingredienti associati alla ricetta
        ingredients_data = self.get_ingredients_data()
        for ingredient_data in ingredients_data:
            ingredient = Ingredient(recipe=recipe, **ingredient_data)
            ingredient.save()

        return super().form_valid(form)

    def get_ingredients_data(self):
        ingredients_data = []
        prefix = self.request.POST.get('ingredient-prefix')
        ingredient_count = int(self.request.POST.get('ingredient-count', 0))

        for i in range(ingredient_count):
            ingredient_data = {
                'name': self.request.POST.get(f'{prefix}-{i}-name'),
                'quantity': self.request.POST.get(f'{prefix}-{i}-quantity')
            }
            ingredients_data.append(ingredient_data)

        return ingredients_data


    def get_success_url(self):
        recipe_pk = self.kwargs['pk']
        return reverse_lazy('instructions-create', kwargs={'pk': recipe_pk})


class InstructionsCreateView(CreateView):
    model = models.Instruction
    fields = ['step']
    template_name = 'recipes/create_recipe_instructions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = models.Recipe.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        recipe_pk = self.kwargs['pk']
        recipe = models.Recipe.objects.get(pk=recipe_pk)
        instruction = form.save(commit=False)
        instruction.recipe = recipe
        instruction.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipes-home')

'''

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    form_class = RecipeForm
    template_name = 'recipes/create_recipe.html'


    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()

        ingredient_names = self.request.POST.getlist('name')
        ingredient_quantities = self.request.POST.getlist('quantity')

        for name, quantity in zip(ingredient_names, ingredient_quantities):
            if name:
                ingredient = models.Ingredient(name=name, quantity=quantity)
                ingredient.save()
                recipe.ingredients.add(ingredient)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipes-home')

    def form_invalid(self, form):
        # Print form errors
        print(form.errors)

        # Print non-field errors
        print(form.non_field_errors())

        # Return the default behavior
        return super().form_invalid(form)

'''
class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'author', 'category', 'description', 'instructions']
    template_name = 'recipes/create_recipe.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def user_recipes(request, username):
    user = User.objects.get(username=username)
    recipes = models.Recipe.objects.filter(user=user)
    return render(request, 'recipes/recipe_list.html', {'user': user, 'recipes': recipes})


