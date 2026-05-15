from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'artist', 'event_date', 'description']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': '제목',
            'event_type': '일정 유형',
            'artist': '아티스트',
            'event_date': '일정 날짜',
            'description': '설명',
        }
