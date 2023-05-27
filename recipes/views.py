from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from . import models
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

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


def about(request):
    return render(request, 'recipes/recipe_detail.html', {'title': 'about page'})   #TODO


class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'


class RecipeDetailView(DetailView):
    model = models.Recipe
    template_name = 'recipes/recipe_detail.html'


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('recipes-home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    form_class = RecipeForm
    template_name = 'recipes/create_recipe.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Create Recipe'))
        return form


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'description']

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
