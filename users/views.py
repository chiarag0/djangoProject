from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from recipes.models import Recipe

from recipes.models import Recipe
from . import forms


def register(request):
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned data is a dictionary
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}, your account has been created, please login.")
            return redirect('user-login')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'users/profile.html', {'recipes': recipes})


@login_required()
def favorite_list(request):
    favorites = request.user.favorites.all()
    return render(request, 'users/favorites.html', {'favorites': favorites})


@login_required()
def add_to_favorites(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
        messages.success(request, f"{recipe.title} has been removed from your favorites.")
    else:
        recipe.favorites.add(request.user)
        messages.success(request, f"{recipe.title} has been added to your favorites.")
    return HttpResponseRedirect(recipe.get_absolute_url())
