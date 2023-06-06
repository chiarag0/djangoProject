from django.urls import path, include
from django.contrib import admin
from users import views as user_views
#from users.views import add_to_favorites

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('register/', user_views.register, name="user-register"),
    #path('recipe/<int:pk>/add-to-favorites/', user_views.add_to_favorites, name='add-to-favorites')


]