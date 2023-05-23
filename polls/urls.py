from django.urls import include, path

urlpatterns = [
    path('api/', include('polls_app.urls')),
]

