from rest_framework import generics, permissions
from .models import Team
from .serializers import TeamSerializer

class TeamDetailView(generics.RetrieveAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Team.objects.get(user=self.request.user)