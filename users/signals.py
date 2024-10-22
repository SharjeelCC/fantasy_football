from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from teams.models import Team
from players.models import Player
import random

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=User)
def create_user_team(sender, instance, created, **kwargs):
    if created:
        # Create a new team for the user
        Team.objects.create(user=instance)
        
@receiver(m2m_changed, sender=Team.players.through)
def update_team_total_value(sender, instance, **kwargs):
    # Recalculate and update the team's total value when the players change
    instance.update_total_value()
    # Save the instance after updating the total_value
    instance.save(update_fields=['total_value'])