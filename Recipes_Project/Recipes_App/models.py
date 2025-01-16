from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

from django.apps import AppConfig
#from CookingRecipes.api import signals

from django.db.models.signals import post_save
from django.dispatch import receiver

class Dietary_Preference(models.Model):
    title = models.CharField(max_length=30)
    about = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

class Recipes(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    ingratiates = models.CharField(max_length=50, null=True, blank= True)
    cooking_style = models.CharField(max_length=50, null=True, blank= True)
    instructions = models.TextField(max_length=200, null=True, blank= True)
    diet = models.ForeignKey(Dietary_Preference, on_delete = models.CASCADE, related_name='diet_options')
    avg_rating = models.FloatField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Reviews(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(max_length=200, null=True, blank=True)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='Rating')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.rating) +   '|'   + self.recipe.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    Dietary_Preferences = models.ManyToManyField(Dietary_Preference, blank=True)
    #profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return str(self.user)
    