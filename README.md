# 🌟 Features

#### User Profiles:
- Users can create and manage their profiles.<br>
- Add dietary preferences to customize recipe suggestions.

#### Recipes:

- View all available recipes with details like ingredients, cooking style, and instructions.<br>
- Add and manage new recipes (admin-only access).

#### Dietary Preferences:

- Manage dietary preference categories such as vegan, vegetarian, gluten-free, etc.<br>
- Link recipes to specific dietary preferences.

#### User Reviews:

- Add ratings and reviews for recipes (1-5 stars).<br>
- Edit and delete reviews for recipes.<br>
- View reviews by individual users.

### REST API Features:

- CRUD functionality for Recipes, Dietary Preferences, and Reviews.<br>
- API endpoints secured with permissions and rate-limiting.<br>
- Pagination, filtering, and searching capabilities for recipes.<br>

### Throttling:

- Custom throttle rates for authenticated users and anonymous users.<br>
- Scoped throttling for specific actions like creating reviews.

## 🛠️ Tech Stack

- Backend: Django, Django REST Framework.<br>
- Database: PostgreSQL.<br>
- Authentication: Django auth with rest_framework.authtoken.<br>
- Libraries Used: django-filter for filtering querysets.<br>
- psycopg2 for PostgreSQL database connectivity.

## 🚀 Installation and Setup Prerequisites:
- Install Python 3.9+.<br>
- Install PostgreSQL and set up a database.<br>

### Steps to Run Locally:

#### Clone the Repository:

- git clone <repository-url> <br>
- cd My-Cooking-App

#### Set Up a Virtual Environment:

- python -m venv myenv <br>
- source myenv/bin/activate   # On Windows: myenv\Scripts\activate

#### Install Dependencies:
- pip install -r requirements.txt

#### Configure the Database:<br>
- Update the DATABASES settings in settings.py with your PostgreSQL credentials:
python
- DATABASES = {<br>
&nbsp;&nbsp;&nbsp;&nbsp;'default': {<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'ENGINE': 'django.db.backends.postgresql',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'NAME': 'RecipesDB',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'USER': 'Bala',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'PASSWORD': '********',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'HOST': 'localhost',<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'PORT': '5432',<br>
&nbsp;&nbsp;&nbsp;&nbsp;}<br>
}<br>

#### Run Migrations:
- python manage.py makemigrations <br>
- python manage.py migrate

#### Create a Superuser (for admin access):
- python manage.py createsuperuser

#### Start the Server:
- python manage.py runserver <br>
- Access the app at http://127.0.0.1:8000.

## 📚 API Endpoints
#### Dietary Preferences:

+ GET /diet/ - List all dietary preferences.

+ POST /diet/ - Add a new dietary preference.

+ GET /diet/<int:pk> - Retrieve a specific dietary preference.

+ PUT /diet/<int:pk> - Update a dietary preference.

+ DELETE /diet/<int:pk> - Delete a dietary preference.

#### Recipes:
+ GET /list/ - List all recipes.

+ POST /list/ - Add a new recipe (admin-only).

+ GET /list/<int:pk> - Retrieve details of a specific recipe.

+ PUT /list/<int:pk> - Update a recipe (admin-only).

+ DELETE /list/<int:pk> - Delete a recipe (admin-only).

#### Reviews:
+ GET /list/<int:pk>/reviews/ - List reviews for a specific recipe.

+ POST /list/<int:pk>/review-create/ - Add a review for a recipe.

+ GET /list/review/<int:pk>/ - Retrieve, update, or delete a specific review.

#### User Profiles:
+ GET/POST/PUT /profile/ - Manage user profiles.

#### User-Specific Reviews:
+ GET /reviews/<str:username>/ - View reviews by a specific user.

## 🧪 Running Tests
To run the tests, execute the following command:
+ python manage.py test

Output example:
Found 21 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................
----------------------------------------------------------------------
Ran 21 tests in 16.008s

OK
Destroying test database for alias 'default'...

## 🌟 Future Enhancements:<br>
- Add a feature to upload and display recipe images.
- Implement OAuth-based authentication (e.g., Google or Facebook login).
- Add notifications for new reviews or recipe updates.
- Optimize API performance with caching.

## 🤝 Credits:<br>
- Developed by: Bala Raju.K<br>
- Framework: Django and Django REST Framework<br>
- Database: PostgreSQL.

## 📄 License
- This project is licensed under the MIT License. See the LICENSE file for details.
