from django.db import models

'''
from django.contrib.auth.models import AbstractUser, Permission, Group

from recipes.models import Recipe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Permission, Group




class User(AbstractUser):
    favorites = models.ManyToManyField(Recipe, related_name='favorited_by', blank=True)

    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',  # Specifica un related_name personalizzato
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',  # Specifica un related_name personalizzato
        related_query_name='user',
    )
'''