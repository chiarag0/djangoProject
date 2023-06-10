from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from . import models
from .forms import RecipeForm, IngredientForm
from django.contrib.auth.decorators import login_required

from .models import Recipe, Ingredient

# Create your views here.

def home(request):
    recipes = models.Recipe.objects.all()
    tags = models.Tag.objects.all()
    context = {
        'recipes': recipes,
        'tags': tags,
    }
    return render(request, 'recipes/home.html', context)



class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']
    paginate_by = 5


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
    fields = ['title', 'category', 'description']
    template_name = 'recipes/create_recipe_start.html'

    def __init__(self):
        super().__init__()
        self.object = None

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print form errors
        print(form.errors)

        # Print non-field errors
        print(form.non_field_errors())

        # Return the default behavior
        return super().form_invalid(form)

    def get_success_url(self):
        pk = self.object.pk
        print(pk)
        return reverse_lazy('ingredients-list', kwargs={'pk': pk})


class IngredientsCreateView(CreateView):
    form_class = IngredientForm
    template_name = 'recipes/create_recipe_ingredients.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = models.Recipe.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        recipe_pk = self.kwargs['pk']
        recipe = Recipe.objects.get(pk=recipe_pk)
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        recipe_pk = self.kwargs['pk']
        return reverse_lazy('ingredients-list', kwargs={'pk': recipe_pk})


class IngredientsListView(ListView):
    model = Ingredient
    template_name = 'recipes/ingredients_list.html'
    context_object_name = 'ingredients'

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        recipe = Recipe.objects.get(pk=recipe_pk)
        return Ingredient.objects.filter(recipe=recipe)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = Recipe.objects.get(pk=self.kwargs['pk'])
        recipe_pk = self.kwargs['pk']
        recipe = Recipe.objects.get(pk=recipe_pk)
        context['ingredients'] = Ingredient.objects.filter(recipe=recipe)
        return context

    def get_success_url(self):
        recipe_pk = self.kwargs['pk']
        return reverse_lazy('instructions-list', kwargs={'pk': recipe_pk})


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
        recipe_pk = self.kwargs['pk']
        return reverse_lazy('instructions-list',  kwargs={'pk': recipe_pk})


class InstructionsListView(ListView):
    model = models.Instruction
    template_name = 'recipes/instructions_list.html'
    context_object_name = 'instructions'

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        recipe = models.Recipe.objects.get(pk=recipe_pk)
        return models.Instruction.objects.filter(recipe=recipe)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = models.Recipe.objects.get(pk=self.kwargs['pk'])
        recipe_pk = self.kwargs['pk']
        recipe = models.Recipe.objects.get(pk=recipe_pk)
        context['instructions'] = models.Instruction.objects.filter(recipe=recipe)
        return context

    def get_success_url(self):
        recipe_pk = self.kwargs['pk']
        return reverse_lazy('recipes-detail', kwargs={'pk': recipe_pk})




class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'author', 'category', 'description', 'instructions']
    template_name = 'recipes/update_recipe.html'   #TODO

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





def SearchByTitle(request):
    query = request.GET.get('query')
    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
    else:
        recipes = Recipe.objects.none()
    return render(request, 'recipes/search_by_title.html', {'recipes': recipes, 'query': query})


def user_recipes(request, username):
    user = User.objects.get(username=username)
    recipes = models.Recipe.objects.filter(user=user)
    return render(request, 'recipes/recipe_list.html', {'user': user, 'recipes': recipes})


