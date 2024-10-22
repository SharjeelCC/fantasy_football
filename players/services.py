from rest_framework.exceptions import ValidationError, NotFound
import random
from django.db import transaction
from decimal import Decimal
from players.repository import get_player_by_id, get_team_by_user, save_player
from players.models import Player, Transaction
from teams.models import Team

def list_player_for_sale(user, player_id, sale_price):
    # Get the player instance from the repository
    player = get_player_by_id(player_id)
    if player is None:
        raise NotFound("Player not found.")

    # Get the user's team from the repository
    user_team = get_team_by_user(user)
    if user_team is None:
        raise ValidationError("User does not have a registered team.")

    # Check if the player belongs to the user's team
    if player.owner_team != user_team:
        raise ValidationError("You can only list players from your own team.")

    # Validate sale price
    if not sale_price or float(sale_price) <= 0:
        raise ValidationError("Sale price must be a positive number.")

    # Mark the player as for sale and set the sale price
    player.for_sale = True
    player.sale_price = sale_price

    # Save the player using the repository
    save_player(player)

    return player

def transfer_player(user, player_id):
    # Fetch the player and ensure it's for sale
    player = Player.objects.filter(id=player_id, for_sale=True).first()
    if not player:
        raise ValidationError("Player is not available for sale.")

    # Get the buyer's and seller's teams
    buyer_team = Team.objects.filter(user=user).first()
    seller_team = player.owner_team

    # Validate the teams
    if not buyer_team:
        raise ValidationError("The buyer does not have a team.")
    if not seller_team:
        raise ValidationError("The seller does not have a valid team.")
    if buyer_team == seller_team:
        raise ValidationError("You already own this player.")
    if buyer_team.capital < player.sale_price:
        raise ValidationError("Insufficient capital to purchase this player.")

    # Perform the transfer in an atomic transaction for consistency
    with transaction.atomic():
        # Deduct the sale price from the buyer's capital
        buyer_team.capital -= player.sale_price
        buyer_team.save(update_fields=['capital'])

        # Add the sale price to the seller's capital
        seller_team.capital += player.sale_price
        seller_team.save(update_fields=['capital'])

        # Update the player's ownership
        sale_price_trans = player.sale_price
        player.owner_team = buyer_team
        player.for_sale = False
        player.sale_price = None

        # Apply a random value increase to the player's value
        value_increase = Decimal(random.uniform(0.05, 0.20))  # Random increase between 5% and 20%
        player.value += player.value * value_increase
        player.save()

        # Update the list of players for both teams
        buyer_team.players.add(player)
        seller_team.players.remove(player)

        # Update the total value of both teams
        buyer_team.update_total_value()
        seller_team.update_total_value()

        # Record the transaction
        transaction_record = Transaction.objects.create(
            buyer=user,
            seller=seller_team.user,
            player=player,
            transfer_amount=sale_price_trans
        )

        # Mark the transaction as inactive
        transaction_record.is_active = False
        transaction_record.save()

    return player, transaction_record