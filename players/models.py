# players/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Define constants for player positions
POSITION_CHOICES = [
    ('GK', 'Goalkeeper'),
    ('DF', 'Defender'),
    ('MF', 'Midfielder'),
    ('FW', 'Forward'),
]

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=1000000)
    for_sale = models.BooleanField(default=False)  # Indicates if the player is available for sale
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    owner_team = models.ForeignKey('teams.Team', null=True, blank=True, on_delete=models.SET_NULL, related_name='owned_players')

    def __str__(self):
        return f"{self.name} ({self.get_position_display()})"

class Transaction(models.Model):
    buyer = models.ForeignKey(User, related_name='bought_transactions', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='sold_transactions', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='transactions', on_delete=models.CASCADE)
    transfer_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transfer_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        if not self.is_active:
            raise ValidationError("Cannot delete inactive transactions.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Transfer of {self.player.name} from {self.seller.username} to {self.buyer.username} for {self.transfer_amount}"
