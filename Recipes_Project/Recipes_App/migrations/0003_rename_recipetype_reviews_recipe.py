# Generated by Django 4.2.17 on 2024-12-29 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes_App', '0002_rename_recipe_reviews_recipetype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='recipetype',
            new_name='recipe',
        ),
    ]
