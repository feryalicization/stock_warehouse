from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ..models import *
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate




class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
        )

        UserProfile.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        # Update other fields
        for attr, value in validated_data.items():
            if attr != 'password':
                setattr(instance, attr, value)
        
        # Handle password update
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()  

        user_profile = getattr(instance, 'userprofile', None)
        if user_profile:
            user_profile.updated_at = timezone.now()
            user_profile.save()

        return instance
    
    def delete(self, instance):
        # Update the deleted_at field in UserProfile
        user_profile = getattr(instance, 'userprofile', None)
        if user_profile:
            user_profile.deleted_at = timezone.now()
            user_profile.save()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)
    is_wedding = serializers.SerializerMethodField() 
    class Meta:
        model = User
        fields = '__all__'

    def get_is_wedding(self, obj):
        return Wedding.objects.filter(user=obj).exists()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # token['email'] = user.email
        # token['username'] = user.username

        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        # Add all user data to the token
        for key, value in user_data.items():
            token[key] = value

        print('token', token)
        return token