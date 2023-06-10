# Generated by Django 4.2.2 on 2023-06-09 10:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0010_tag_recipe_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
