import json
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Avg

from .models import Survey, Question, Response, Answer
from .forms import SurveyRespondForm, SurveyCreateForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """staff 전용 뷰 — 비staff 접근 시 403."""
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


class SurveyListView(ListView):
    model = Survey
    template_name = 'surveys/list.html'
    context_object_name = 'surveys'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_surveys = Survey.objects.all()
        ctx['active_surveys'] = [s for s in all_surveys if s.is_active]
        ctx['closed_surveys'] = [s for s in all_surveys if not s.is_active]
        return ctx


class SurveyRespondView(LoginRequiredMixin, TemplateView):
    template_name = 'surveys/respond.html'

    def get_survey(self):
        return get_object_or_404(Survey, pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            survey = self.get_survey()
            # 이미 응답한 유저 → results로 redirect
            if Response.objects.filter(survey=survey, respondent=request.user).exists():
                return redirect(reverse('surveys:results', kwargs={'pk': survey.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        survey = self.get_survey()
        ctx['survey'] = survey
        ctx['form'] = SurveyRespondForm(survey=survey)
        return ctx

    def post(self, request, *args, **kwargs):
        survey = self.get_survey()

        # 이미 응답했으면 redirect (POST 재전송 방어)
        if Response.objects.filter(survey=survey, respondent=request.user).exists():
            return redirect(reverse('surveys:results', kwargs={'pk': survey.pk}))

        form = SurveyRespondForm(survey=survey, data=request.POST)
        if form.is_valid():
            response_obj = Response.objects.create(
                survey=survey,
                respondent=request.user,
            )
            for question in survey.questions.all():
                field_name = f'question_{question.pk}'
                answer_text = form.get_answer_text(field_name)
                Answer.objects.create(
                    response=response_obj,
                    question=question,
                    answer_text=answer_text,
                )
            messages.success(request, '응답이 제출되었습니다.')
            return redirect(reverse('surveys:list'))
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        survey = self.get_survey()
        ctx['survey'] = survey
        if 'form' not in kwargs:
            ctx['form'] = SurveyRespondForm(survey=survey)
        else:
            ctx['form'] = kwargs['form']
        return ctx


class SurveyCreateView(StaffRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyCreateForm
    template_name = 'surveys/create.html'
    success_url = reverse_lazy('surveys:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        survey = self.object

        # POST에서 동적 질문 파싱
        idx = 0
        while True:
            text_key = f'question_text_{idx}'
            type_key = f'question_type_{idx}'
            if text_key not in self.request.POST:
                break
            text = self.request.POST.get(text_key, '').strip()
            qtype = self.request.POST.get(type_key, 'TEXT')
            options_raw = self.request.POST.get(f'question_options_{idx}', '')
            options = [o.strip() for o in options_raw.splitlines() if o.strip()]
            if text:
                Question.objects.create(
                    survey=survey,
                    text=text,
                    question_type=qtype,
                    options=options,
                    order=idx,
                )
            idx += 1

        messages.success(self.request, '설문이 생성되었습니다.')
        return response


class SurveyResultsView(StaffRequiredMixin, DetailView):
    model = Survey
    template_name = 'surveys/results.html'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        survey = self.object
        stats = []

        for question in survey.questions.all():
            answers = Answer.objects.filter(question=question)
            q_stat = {
                'question': question,
                'answers': answers,
                'answer_count': answers.count(),
            }

            if question.question_type in ('CHOICE', 'MULTIPLE'):
                # 선택지별 카운트 및 비율
                option_counts = {}
                for opt in question.options:
                    option_counts[opt] = 0

                for answer in answers:
                    if question.question_type == 'MULTIPLE':
                        try:
                            selected = json.loads(answer.answer_text)
                        except (json.JSONDecodeError, TypeError):
                            selected = []
                    else:
                        selected = [answer.answer_text]

                    for sel in selected:
                        if sel in option_counts:
                            option_counts[sel] += 1

                total = sum(option_counts.values()) or 1
                q_stat['option_stats'] = [
                    {
                        'option': opt,
                        'count': cnt,
                        'percent': round(cnt / total * 100),
                    }
                    for opt, cnt in option_counts.items()
                ]

            elif question.question_type == 'SCALE':
                values = []
                for answer in answers:
                    try:
                        values.append(int(answer.answer_text))
                    except (ValueError, TypeError):
                        pass
                q_stat['scale_avg'] = round(sum(values) / len(values), 2) if values else 0

            stats.append(q_stat)

        ctx['stats'] = stats
        ctx['responses'] = survey.responses.select_related('respondent').all()
        return ctx


class SurveyResponseDetailView(StaffRequiredMixin, DetailView):
    model = Response
    template_name = 'surveys/response_detail.html'
    context_object_name = 'response'
    pk_url_kwarg = 'response_pk'

    def get_queryset(self):
        survey_pk = self.kwargs['pk']
        return Response.objects.filter(survey_id=survey_pk).select_related('respondent', 'survey')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        response_obj = self.object
        ctx['survey'] = response_obj.survey
        ctx['answer_pairs'] = [
            {'question': a.question, 'answer': a}
            for a in response_obj.answers.select_related('question').order_by('question__order')
        ]
        return ctx
