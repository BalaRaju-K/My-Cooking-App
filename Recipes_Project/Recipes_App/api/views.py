from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def sample(Request):
    return HttpResponse('This is a sample view')

from Recipes_App.models import Recipes, Reviews, Dietary_Preference, Profile
from Recipes_App.api.serializers import (RecipesSerializer, ReviewsSerializer, 
                                            Dietary_PreferenceSerializer, ProfileSerializer)

from Recipes_App.api.permissions import IsAdminReadOnly, IsReviewUserOrReadOnly, IsProfileOwner
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.exceptions import ValidationError
from rest_framework import viewsets

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from Recipes_App.api.throttling import ReviewListThrottle, ReviewCreateThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from Recipes_App.api.paginations import ReviewListPagination, RecipeListPagination, DietListPagination

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated] #, IsProfileOwner

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if Profile.objects.filter(user=request.user).exists():
            return Response({"detail": "Profile already exists for this user."},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"detail": "You do not have permission to update this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewUser(generics.ListAPIView):
    serializer_class = ReviewsSerializer
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Reviews.objects.filter(review_user__username = username)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle]
    #pagination_class = ReviewListPagination
    
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(recipe = pk)
 
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Reviews.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        one = Recipes.objects.get(pk = pk)
        
        four = self.request.user
        review_queryset = Reviews.objects.filter(recipe=one, review_user = four)
        
        if review_queryset.exists():
            raise ValidationError("User has already reviewed this recipe.")
        
        if one.total_ratings == 0:
            one.avg_rating = serializer.validated_data['rating']
        else:
            one.avg_rating = (one.avg_rating * one.total_ratings + serializer.validated_data['rating']) / (one.total_ratings + 1 )
        
        
        one.total_ratings = one.total_ratings + 1
        one.save()    
        return serializer.save(recipe = one, review_user = four)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class RecipeListNew(generics.ListCreateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [IsAdminReadOnly]
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['diet__title', 'name']
    #pagination_class = RecipeListPagination

    
class RecipeList(APIView):
    permission_classes = [IsAdminReadOnly]
    #pagination_class = RecipeListPagination
    def get(self, request):
            recipes = Recipes.objects.all()
            serializer = RecipesSerializer(recipes, many=True)
            return Response(serializer.data)
        

    def post(self, request):
        serializer = RecipesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class RecipeDetail(APIView):
    permission_classes = [IsAdminReadOnly]
    #pagination_class = RecipeDetailPagination
    
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    def get(self, request, pk):
        try:
            one =  Recipes.objects.get(pk=pk)
            serializer_one = RecipesSerializer(one)
            return Response(serializer_one.data)
        except Recipes.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
    
    def put(self, request, pk):
        serializer = RecipesSerializer(data = request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def delete(self, request, pk):
        recipe = Recipes.objects.get(pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)           

class DietLisT(APIView):
    permission_classes = [IsAdminReadOnly]
    #pagination_class = DietListPagination
    def get(self, request):
        try:
            queryset = Dietary_Preference.objects.all()
            serializer = Dietary_PreferenceSerializer(queryset, many=True)
            return Response(serializer.data)
        except Dietary_Preference.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
    def post(self, request):
        serializer = Dietary_PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class DietDetail(APIView):
    permission_classes = [IsAdminReadOnly]
    def get(self, request, pk):
        try:
            one = Dietary_Preference.objects.get(pk=pk)
            serializer_one = Dietary_PreferenceSerializer(one)
            return Response(serializer_one.data)
        except Dietary_Preference.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
    
    def put(self, request, pk):
        two = Dietary_Preference.objects.get(pk=pk)
        serializer = Dietary_PreferenceSerializer(two, data = request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        diet = Dietary_Preference.objects.get(pk=pk)
        diet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        