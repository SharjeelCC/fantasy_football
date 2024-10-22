from players.models import Player, Transaction
from teams.models import Team
from django.core.exceptions import ObjectDoesNotExist

def get_player_by_id(player_id):
    """
    Retrieve a player by its ID.
    """
    try:
        return Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return None

def get_team_by_user(user):
    """
    Retrieve a team associated with a given user.
    """
    try:
        return Team.objects.get(user=user)
    except Team.DoesNotExist:
        return None

def get_player_for_sale(player_id):
    return Player.objects.filter(id=player_id, for_sale=True).first()

def save_player(player):
    """
    Save the player instance.
    """
    player.save()

def list_players_for_team(team):
    """
    List all players belonging to a specific team.
    """
    return Player.objects.filter(owner_team=team)

def create_transaction(buyer, seller, player, amount):
    return Transaction.objects.create(buyer=buyer, seller=seller, player=player, transfer_amount=amount)