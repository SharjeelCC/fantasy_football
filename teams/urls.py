from django.urls import path
from .views import TeamDetailView

urlpatterns = [
    path('team/', TeamDetailView.as_view(), name='team-detail'),
]