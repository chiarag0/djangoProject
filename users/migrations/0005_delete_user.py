# Generated by Django 4.2.2 on 2023-06-09 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_password_user_username_alter_user_favorites'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
