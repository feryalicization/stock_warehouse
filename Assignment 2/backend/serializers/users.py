from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        # Add all user data to the token
        for key, value in user_data.items():
            token[key] = value

        print('token', token)
        return token
