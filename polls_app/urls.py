from django.urls import path, include
from polls_app.views import UserListAPIView, UserDetailAPIView, UserRegistrationAPIView, UserLoginAPIView, PollViewSet, PollChoiceViewSet
from rest_framework import routers
from polls_app.views import PollChoiceUpdateView, LogoutAPIView, PollsByUserViewSet

router = routers.DefaultRouter()
router.register(r'all', PollViewSet)
router.register(r'dashboard', PollsByUserViewSet)

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('users/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('users/logout/', LogoutAPIView.as_view(), name='logout'),
    path('choices/<int:pk>/', PollChoiceUpdateView.as_view(), name='choice-update'),
    path('polls/', include(router.urls)),
    
]