from rest_framework import viewsets
from polls_app.models import Poll, PollChoice
from polls_app.serializers import PollSerializer, PollChoiceSerializer

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from polls_app.models import CustomUser
from rest_framework import generics
from polls_app.serializers import UserSerializer, RegistrationSerializer
from dj_rest_auth.views import LoginView

from rest_framework import generics, permissions




from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from polls_app.models import PollChoice
from polls_app.serializers import PollChoiceSerializer

from django.contrib.auth import logout
from django.http import JsonResponse
from django.views import View

import datetime

from .authentication import CustomTokenAuthentication

class LogoutAPIView(View):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.last_logout = datetime.now()
        user.save()
        return Response({"detail": "Logout successful"})
    
    
class PollChoiceUpdateView(generics.UpdateAPIView):

    queryset = PollChoice.objects.all()
    serializer_class = PollChoiceSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    # def put(self, request, choice_id):

    #     # Fetch the specific PollChoice object
    #     poll_choice = get_object_or_404(PollChoice, id=choice_id)


    #     # Update the fields of the PollChoice object
    #     serializer = PollChoiceSerializer(poll_choice, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=400)



# classes for poll crud
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def retrieve(self, request, *args, **kwargs):
        super().retrieve(self, request, *args, **kwargs)
    

# class to return polls by the logged in user
# classes for poll crud
class PollsByUserViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user

        print(user)

        # Filter the polls based on the user
        queryset = Poll.objects.filter(user=user)

        return queryset



    


class PollChoiceViewSet(viewsets.ModelViewSet):
    queryset = PollChoice.objects.all()
    serializer_class = PollChoiceSerializer

    


# classes for user CRUD


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    authentication_classes = []  # Disable authentication for user registration
    permission_classes = [permissions.AllowAny]  # Allow any user to register

class UserLoginAPIView(LoginView):
    permission_classes = [permissions.AllowAny]

# class UserListCreateAPIView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer