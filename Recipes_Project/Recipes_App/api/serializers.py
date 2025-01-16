from rest_framework import serializers
from Recipes_App.models import Recipes, Reviews, Dietary_Preference, Profile
from django.contrib.auth.models import User

class ReviewsSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        #fields = '__all__'
        #exclude = ('recipe', )
        fields = ['review_user', 'rating', 'comments', 'active', 'recipe']
        extra_kwargs = {
            'recipe': {'required': False},
        }

class RecipesSerializer(serializers.ModelSerializer):
    Rating = ReviewsSerializer(many=True, read_only=True)
    class Meta:
        model = Recipes
        fields = '__all__'

class Dietary_PreferenceSerializer(serializers.ModelSerializer):
    diet_options = RecipesSerializer(many=True, read_only=True)
    class Meta:
        model = Dietary_Preference
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Profile
        fields = ['user', 'Dietary_Preferences', 'bio']
