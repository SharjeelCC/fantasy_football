from rest_framework import serializers
from .models import Team
from players.models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'value']
        read_only_fields = ['value']

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'capital', 'players', 'total_value']
        read_only_fields = ['capital', 'total_value'] 