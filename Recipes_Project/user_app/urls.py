from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.views import Register, logout, DeleteUserView

urlpatterns = [
    path('login/', obtain_auth_token, name="login"),
    path('register/', Register.as_view(), name="register"),
    path('logout/', logout, name='logout' ),
    path('delete_user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user' ),
]
