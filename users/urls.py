from django.urls import path, include
from django.contrib import admin
from users import views as user_views
from recipes import views as recipes_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('register/', user_views.register, name="user-register"),
    path('fav/<int:id>', user_views.add_to_favorites, name='add-to-favorites'),
    path('profile/favorites/', user_views.favorite_list, name='favorite-list'),
    path('recipe/<int:pk>', recipes_views.RecipeDetailView.as_view(), name="recipes-detail"),

]