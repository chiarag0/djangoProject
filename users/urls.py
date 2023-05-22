from django.urls import path, include
from django.contrib import admin
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('register/', user_views.register, name="user-register"),
]