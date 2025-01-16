from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Recipes_App.api.views import (DietLisT, DietDetail, 
                                   RecipeList, RecipeDetail, 
                                   ReviewList, ReviewCreate, ReviewDetail,
                                   ReviewUser, RecipeListNew, ProfileViewSet)


router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('diet/' , DietLisT.as_view(), name ="DietLisT"),
    path('diet/<int:pk>' , DietDetail.as_view(), name ="DietDetail"),
    
    path('list/' , RecipeList.as_view(), name ="RecipeList"),
    path('list/<int:pk>' , RecipeDetail.as_view(), name ="RecipeDetail"),
    
    path('list/<int:pk>/reviews/' , ReviewList.as_view(), name ="ReviewList"),
    path('list/<int:pk>/review-create/' , ReviewCreate.as_view(), name ="review-create"),
    path('list/review/<int:pk>/' , ReviewDetail.as_view(), name ="ReviewDetail"),
    
    path('reviews/<str:username>/', ReviewUser.as_view(), name='ReviewUser'),
    path('newlist/', RecipeListNew.as_view(), name="RecipeListNew"),
    
    path('', include(router.urls)),
]