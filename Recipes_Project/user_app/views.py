from django.shortcuts import render
from user_app.serializers import RegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def delete(self, request, user_id):
        try:
            if not request.user.is_staff:
                return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        return Response(status=status.HTTP_200_OK)

class Register(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            if account is None:
                raise ValueError("User Creation Failed")
            token, created = Token.objects.get_or_create(user=account)
            
            data['response'] = "User registration successful"
            data['username'] = account.username
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    