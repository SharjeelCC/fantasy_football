from decimal import Decimal
import pytest
from django.contrib.auth.models import User
from players.models import Player, Transaction
from teams.models import Team
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    return User.objects.create_user(username="testuser", password="testpass")

@pytest.fixture
def create_player(create_team):
    def _create_player(owner_team, name="Test Player", position="MF", value=Decimal('1000000')):
        player = Player.objects.create(
            name=name,
            position=position,
            value=value,
            owner_team=owner_team
        )
        return player
    return _create_player

@pytest.fixture
def create_team(create_user):
    # Ensure no existing team for the user before creating
    Team.objects.filter(user=create_user).delete()
    # Create a new team associated with the user
    return Team.objects.create(user=create_user)

@pytest.mark.django_db
def test_list_player_for_sale(api_client, create_team):
    # Authenticate the client
    user = create_team.user
    api_client.force_authenticate(user=user)

    # List one of the created players for sale
    player = create_team.players.first()
    response = api_client.post(f"/api/players/{player.id}/list-for-sale/", {"sale_price": "1000000.00"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["player"]["id"] == player.id
    assert response.data["player"]["for_sale"] is True
    assert response.data["player"]["sale_price"] == "1000000.00"

@pytest.mark.django_db
def test_player_transfer(api_client, create_team):
    # Create a user and authenticate
    user = create_team.user
    api_client.force_authenticate(user=user)

    # Create another team to simulate a transfer
    other_user, _ = User.objects.get_or_create(username='otheruser', password='otherpassword')
    other_team, _ = Team.objects.get_or_create(user=other_user)

    # Create a player associated with the other team
    player = Player.objects.create(name='Transfer Player', position='DF', owner_team=other_team, for_sale=True, sale_price='500000.00')

    # Perform the transfer
    url = f'/api/players/transfer/{player.id}/'
    response = api_client.post(url, format='json')

    # Assert the transfer response
    assert response.status_code == 200
    assert response.data['status'] == 'success'
    assert response.data['message'] == 'Player transfer completed successfully.'
    assert response.data['data']['player']['new_owner_team'] == create_team.name

@pytest.mark.django_db
def test_transaction_history(api_client, create_user, create_team, create_player):
    # Create a user and authenticate
    user = create_team.user
    api_client.force_authenticate(user=user)
    
    # Create a team and a player
    team = create_team
    player = Player.objects.create(name='Transfer Player', position='DF', owner_team=team, for_sale=True, sale_price='500000.00')
    
    # Create a transaction for the player
    Transaction.objects.create(
        buyer=user,
        seller=user,
        player=player,
        transfer_amount=Decimal('1000000')
    )
    
    # Get the transaction history
    response = api_client.get("/api/players/transactions/")
    print(player)
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]["buyer"] == user.username
    assert response.data[0]["player"]["id"] == player.id