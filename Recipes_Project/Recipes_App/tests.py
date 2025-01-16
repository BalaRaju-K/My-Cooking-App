from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from Recipes_App import models

class Dietary_PreferenceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'token' + self.token.key)
        self.diettype = models.Dietary_Preference.objects.create(title = 'Non-Veg',
            about = 'All the information about this preference')
     
    def test_diet_create(self):
        url = reverse('DietLisT')
        data = {
            'title': 'Non-Veg',
            'about' : 'All the information about this preference'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_diet_List(self):
        response = self.client.get(reverse('DietLisT'))    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_diet_detail(self):        
        response = self.client.get(reverse('DietDetail', args=[self.diettype.id, ]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class RecipesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'token' + self.token.key)
        self.diettype = models.Dietary_Preference.objects.create(title = 'Non-Veg',
            about = 'All the information about this preference')
        self.diettype2 = models.Dietary_Preference.objects.create(title = 'Veg',
            about = 'All the information about this preference')
        self.recipe= models.Recipes.objects.create(
            name = 'Egg Biriyani',
            ingratiates = 'EGGS',
            cooking_style = 'Hyderabad-style' ,
            instructions = 'Old_ways',
            diet = self.diettype2,
            active = True
        )
     
    def test_recipes_create(self):
        url = reverse('RecipeList')
        data = {
            'name': 'Chicken Biriyani',
            'ingratiates' : 'Masala',
            'cooking_style' : 'Dhaba-style' ,
            'instructions' : '',
            'diet': self.diettype,
            'active' : True
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_recipes_list(self):
        response = self.client.get(reverse('RecipeList'))    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_detail(self):        
        response = self.client.get(reverse('RecipeDetail', args=[self.recipe.id, ]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class ReviewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example2', password='example2@123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.diet = models.Dietary_Preference.objects.create(title="Non-Veg", about="Eats")
        self.recipe1 = models.Recipes.objects.create(
            name="Chicken Biriyani",
            ingratiates="MASALA",
            cooking_style="KMM",
            instructions="MyStyle",
            diet=self.diet,
            active=True
        )
    
        self.recipe2 = models.Recipes.objects.create(
            name="Egg Biriyani",
            ingratiates="MASALA",
            cooking_style="HYD",
            instructions="MyStyle",
            diet=self.diet,
            active=True
        )
        self.review = models.Reviews.objects.create(review_user=self.user,
                                            rating=2,
                                            comments="Best",
                                            active=True,
                                            recipe=self.recipe2)
    def test_Reviews_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "comments": "Super",
            "active": True,
            "recipe" : self.recipe1.id
        }
        response = self.client.post(reverse("review-create", args=[self.recipe1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_Review_list(self):
        response = self.client.get(reverse('ReviewList', args=[self.recipe1.id]))
        self.assertEqual(response.status_code, 200)

    def test_Review_detail(self):
        response = self.client.get(reverse('ReviewDetail', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_Review_update(self):
        data = {
            "rating": 3,
                "comment": "Changed my mind. It's average.",
                "active": True
            }
        response = self.client.put(reverse('ReviewDetail', args=[self.review.id]), data)
        self.assertEqual(response.status_code, 200)
    
    def test_Review_delete(self):
        response = self.client.delete(reverse('ReviewDetail', args=[self.review.id]))
        self.assertEqual(response.status_code, 204)
    
    def test_Review_User(self):
        url = reverse('ReviewUser', args=[self.user.username])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response = self.client.get(reverse('ReviewUser')+ self.user.username)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class RecipeListNewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.diet = models.Dietary_Preference.objects.create(title="Veg", about="Eats")
        self.recipe1 = models.Recipes.objects.create(
            name="EGG Biriyani",
            ingratiates="MASALA",
            cooking_style="KMM",
            instructions="MyStyle",
            diet=self.diet,
            active=True
        )
        self.recipes2 = models.Recipes.objects.create(
            name="EGG Omllet",
            ingratiates="MASALA",
            cooking_style="KMM",
            instructions="MyStyle",
            diet=self.diet,
            active=True
        )
    
    def test_Recipes_retrieval(self):
        response = self.client.get(reverse('RecipeListNew'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_Recipes_search_filter(self):
        response = self.client.get(reverse('RecipeListNew'), {'search': 'veg'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_watchlist_ordering(self):
    #     response = self.client.get(reverse('WatchListNew'), {'ordering': 'avg_reviews'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Check if movies are ordered by avg_reviews
    #     avg_reviews = [movie['avg_reviews'] for movie in response.data['results']]
    #     self.assertEqual(avg_reviews, sorted(avg_reviews))  


class ProfileTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.diet1 = models.Dietary_Preference.objects.create(title="Vegetarian", about="No meat.")
        self.diet2 = models.Dietary_Preference.objects.create(title="Gluten-Free", about="No gluten.")

        self.profile = models.Profile.objects.create(user=self.user)
        self.client.login(username="testuser", password="password123")

    def test_retrieve_own_profile(self):
        response = self.client.get(reverse('profile-detail', args=[self.profile.id]))
        # print("Status Code:", response.status_code) 
        # print("Response Data:", response.data)     
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['bio'], "")

    def test_update_profile_bio(self):
        data = {'bio': 'I love cooking and sharing recipes!'}
        response = self.client.patch(reverse('profile-detail', args=[self.profile.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_dietary_preferences(self):
        data = {'dietary_preferences': [self.diet1.id, self.diet2.id]}
        response = self.client.patch(reverse('profile-detail', args=[self.profile.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_single_dietary_preference(self):
        data = {'dietary_preferences': [self.diet1.id]}
        response = self.client.patch(reverse('profile-detail', args=[self.profile.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
