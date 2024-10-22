from rest_framework import serializers
from .models import Player, Transaction

class PlayerForSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'value', 'sale_price', 'owner_team']

class TransactionSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()
    player = serializers.StringRelatedField()
    
    class Meta:
        model = Transaction
        fields = ['buyer', 'seller', 'player', 'transfer_amount', 'transfer_date']