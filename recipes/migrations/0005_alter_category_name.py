# Generated by Django 4.1 on 2023-05-30 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0004_alter_ingredient_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("Easy", "Easy"),
                    ("Medium", "Medium"),
                    ("Challenging", "Challenging"),
                ],
                max_length=100,
            ),
        ),
    ]
