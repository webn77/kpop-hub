import json
from django import forms
from .models import Survey, Question


class SurveyRespondForm(forms.Form):
    """Survey의 Question 목록 기반으로 동적으로 필드를 생성하는 폼."""

    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey

        for question in survey.questions.all():
            field_name = f'question_{question.pk}'
            field = self._build_field(question)
            self.fields[field_name] = field

    def _build_field(self, question):
        qtype = question.question_type
        required = question.required
        label = question.text

        if qtype == 'TEXT':
            return forms.CharField(
                label=label,
                required=required,
                widget=forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            )
        elif qtype == 'TEXTAREA':
            return forms.CharField(
                label=label,
                required=required,
                widget=forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2', 'rows': 4}),
            )
        elif qtype == 'CHOICE':
            choices = [(opt, opt) for opt in question.options]
            return forms.ChoiceField(
                label=label,
                required=required,
                choices=choices,
                widget=forms.RadioSelect,
            )
        elif qtype == 'MULTIPLE':
            choices = [(opt, opt) for opt in question.options]
            return forms.MultipleChoiceField(
                label=label,
                required=required,
                choices=choices,
                widget=forms.CheckboxSelectMultiple,
            )
        elif qtype == 'SCALE':
            choices = [(str(i), str(i)) for i in range(1, 6)]
            return forms.ChoiceField(
                label=label,
                required=required,
                choices=choices,
                widget=forms.RadioSelect,
            )
        else:
            return forms.CharField(label=label, required=required)

    def get_answer_text(self, field_name):
        """cleaned_data에서 answer_text 문자열로 변환."""
        value = self.cleaned_data.get(field_name, '')
        if isinstance(value, list):
            return json.dumps(value, ensure_ascii=False)
        return str(value)


class SurveyCreateForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'is_anonymous', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2', 'rows': 3}),
            'expires_at': forms.DateTimeInput(
                attrs={'class': 'w-full border rounded px-3 py-2', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }
