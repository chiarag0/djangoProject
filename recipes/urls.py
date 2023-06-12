
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name="recipes-home"),
    path('', include('users.urls')),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name="recipes-detail"),
    path('recipe/create', views.RecipeCreateView.as_view(), name="recipes-create"),
    path('recipe/<int:pk>/ingredients/create/', views.IngredientsCreateView.as_view(), name="ingredients-create"),
    path('recipe/<int:pk>/ingredients/update/', views.IngredientsListView.as_view(), name="ingredients-list"),
    path('recipe/<int:pk>/instructions/create/', views.InstructionsCreateView.as_view(), name="instructions-create"),
    path('recipe/<int:pk>/instructions/update/', views.InstructionsListView.as_view(), name="instructions-list"),
    path('recipe/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipes-delete"),
    path('user/<str:username>/', views.user_recipes, name='user_recipes'),
    path('search-by-title/', views.SearchByTitle, name='search-by-title'),

]
