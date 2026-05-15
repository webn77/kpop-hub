from django.contrib import admin
from .models import Poll, PollChoice, PollVote


class PollChoiceInline(admin.TabularInline):
    model = PollChoice
    extra = 3


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'end_date', 'total_votes', 'created_at']
    list_filter = ['is_multiple']
    search_fields = ['title', 'description']
    inlines = [PollChoiceInline]


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'choice', 'created_at']
