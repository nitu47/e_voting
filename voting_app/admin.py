from django.contrib import admin
from .models import Voter, Candidate

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_verified', 'has_voted', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'votes')
    search_fields = ('name', 'party')
