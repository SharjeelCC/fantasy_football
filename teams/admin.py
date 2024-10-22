# teams/admin.py
from django.contrib import admin
from .models import Team
from players.models import Player
from django import forms

class TeamAdminForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Filter the queryset to show only players associated with the team
            self.fields['players'].queryset = self.instance.players.all()
        else:
            # If creating a new team, no players should be available initially
            self.fields['players'].queryset = Player.objects.none()

class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm

admin.site.register(Team, TeamAdmin)
