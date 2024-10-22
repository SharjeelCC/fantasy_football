from django.shortcuts import render
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.db import transaction
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from players.models import Player, Transaction
from teams.models import Team
from .serializers import PlayerForSaleSerializer, TransactionSerializer
from players.services import list_player_for_sale, transfer_player
from rest_framework.exceptions import ValidationError

class ListPlayerForSaleView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this endpoint

    def post(self, request, player_id):
        try:
            # Get the sale price from the request data
            sale_price = request.data.get('sale_price')

            # Call the service to list the player for sale
            player = list_player_for_sale(request.user, player_id, sale_price)

            # Return a success response with the player's information
            return Response(
                {
                    "message": "Player listed for sale successfully.",
                    "player": {
                        "id": player.id,
                        "name": player.name,
                        "position": player.position,
                        "sale_price": player.sale_price,
                        "for_sale": player.for_sale,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any unexpected exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlayersForSaleListView(generics.ListAPIView):
    queryset = Player.objects.filter(for_sale=True)  # Filter players marked as for sale
    serializer_class = PlayerForSaleSerializer
    permission_classes = [IsAuthenticated]

class PlayerTransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, player_id):
        user = request.user

        try:
            # Perform the player transfer using the service layer
            player, transaction_record = transfer_player(user, player_id)

            # Return a success response
            response_data = {
                "status": "success",
                "message": "Player transfer completed successfully.",
                "data": {
                    "player": {
                        "id": player.id,
                        "name": player.name,
                        "position": player.position,
                        "new_value": player.value,
                        "new_owner_team": player.owner_team.name,
                    },
                    "transaction": {
                        "id": transaction_record.id,
                        "buyer": transaction_record.buyer.username,
                        "seller": transaction_record.seller.username,
                        "transfer_amount": transaction_record.transfer_amount,
                        "is_active": transaction_record.is_active,
                    },
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Handle validation errors
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any unexpected exceptions
            return Response({"status": "error", "message": "An unexpected error occurred.", "errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionHistoryView(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by('-transfer_date')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(buyer=user) | Transaction.objects.filter(seller=user)
