from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


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


'''
@login_required
def add_to_favorites(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    request.user.favorites.add(recipe)
    return redirect('recipe-detail', pk=pk)


def view_favorites(request):
    favorites = request.user.favorites.all()
    return render(request, 'recipes/../templates/users/favorites.html', {'favorites': favorites}) '''