from django.db import models
from django.contrib.auth.models import User
from players.models import Player

class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    capital = models.DecimalField(max_digits=15, decimal_places=2, default=5000000)
    players = models.ManyToManyField(Player, blank=True, related_name='teams')
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Check if the object is being created for the first time
        if not self.pk:
            self.name = f"{self.user.username}'s Team"
            super().save(*args, **kwargs)  # Save the team first to get an ID
            self.generate_players()  # Generate players after the team has been saved
        
        # Update the total value of the team
        self.update_total_value()
        super().save(update_fields=['total_value', 'capital'])  # Save only the total_value update

    def generate_players(self):
        # Ensure that no players are added if the team already has players
        if self.players.count() == 0:
            # Define positions: 2 Goalkeepers, 6 Defenders, 6 Midfielders, 6 Forwards
            positions = ['GK'] * 2 + ['DF'] * 6 + ['MF'] * 6 + ['FW'] * 6
            for i, position in enumerate(positions):
                player_name = f"Player {self.user.username} {i+1}"
                # Create a new player and add it to the team's player list
                player = Player.objects.create(name=player_name, position=position, owner_team=self)
                self.players.add(player)  # Associate the player with this team

    def update_total_value(self):
        # Calculate the total value based on player values
        new_total_value = sum(player.value for player in self.players.all())
        # Update the instance's total_value field directly
        self.total_value = new_total_value

    def __str__(self):
        return self.name
