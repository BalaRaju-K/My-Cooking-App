from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def save(self):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        email = self.validated_data.get('email', '')
            
            
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
            
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
            
        account = User.objects.create_user(
                username=username,
                email=email,
                password=password
                )
        return account