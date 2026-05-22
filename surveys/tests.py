from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from .models import Survey, Question, Response, Answer

User = get_user_model()


class SurveyRespondOnceTest(TestCase):
    """같은 유저가 두 번 응답 시 두 번째는 중복 방지."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234!')
        self.survey = Survey.objects.create(
            title='테스트 설문',
            created_by=self.user,
        )
        self.question = Question.objects.create(
            survey=self.survey,
            text='좋아하는 색깔은?',
            question_type='TEXT',
            order=0,
        )

    def test_survey_respond_once_per_user(self):
        self.client.login(username='testuser', password='pass1234!')
        url = reverse('surveys:respond', kwargs={'pk': self.survey.pk})

        # 첫 번째 응답
        self.client.post(url, {f'question_{self.question.pk}': '파란색'})

        # 두 번째 요청 — redirect 확인
        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('surveys:results', kwargs={'pk': self.survey.pk}),
            fetch_redirect_response=False,
        )

        # 응답 중복 없이 1개만 존재
        self.assertEqual(
            Response.objects.filter(survey=self.survey, respondent=self.user).count(),
            1,
        )


class SurveyResultsStaffOnlyTest(TestCase):
    """일반 유저 results 접근 → 403."""

    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff', password='pass1234!', is_staff=True, nickname='staff_nick'
        )
        self.normal_user = User.objects.create_user(
            username='normal', password='pass1234!', nickname='normal_nick'
        )
        self.survey = Survey.objects.create(
            title='스태프 전용 설문',
            created_by=self.staff,
        )

    def test_survey_results_requires_staff(self):
        self.client.login(username='normal', password='pass1234!')
        url = reverse('surveys:results', kwargs={'pk': self.survey.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class SurveyRespondLoginRequiredTest(TestCase):
    """미로그인 응답 → 302 redirect."""

    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='pass1234!')
        self.survey = Survey.objects.create(
            title='로그인 필요 설문',
            created_by=self.user,
        )

    def test_survey_respond_requires_login(self):
        url = reverse('surveys:respond', kwargs={'pk': self.survey.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])
