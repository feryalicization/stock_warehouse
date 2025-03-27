from rest_framework import generics
from ..models import *
from ..serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializers.users import *
from rest_framework_simplejwt.views import TokenObtainPairView



class UserRegistrationView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)
    
class UserEditView(generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer