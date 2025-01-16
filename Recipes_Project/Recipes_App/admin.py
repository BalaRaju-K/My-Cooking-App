from django.contrib import admin
from Recipes_App.models import Recipes, Reviews, Dietary_Preference, Profile

admin.site.register(Recipes)
admin.site.register(Reviews)
admin.site.register(Dietary_Preference)
admin.site.register(Profile)
