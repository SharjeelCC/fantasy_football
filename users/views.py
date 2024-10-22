from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserProfileSerializer

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer  # Keep this as before
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer  # Keep this as before
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        user = self.get_object()  # Get the user object
        serializer = self.get_serializer(user, data=request.data, partial=True)  # Allow partial updates
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Save the updated user data
        return Response(serializer.data)  # Return the updated data


