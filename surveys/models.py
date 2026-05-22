from django.db import models
from django.conf import settings
from django.utils import timezone


class Survey(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    description = models.TextField(blank=True, verbose_name='설명')
    is_anonymous = models.BooleanField(default=False, verbose_name='익명 응답')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='마감일')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_surveys',
        verbose_name='작성자',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '설문조사'
        verbose_name_plural = '설문조사 목록'

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        return self.expires_at is None or self.expires_at > timezone.now()

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def response_count(self):
        return self.responses.count()


class Question(models.Model):
    QUESTION_TYPES = [
        ('TEXT', '주관식 단답'),
        ('TEXTAREA', '주관식 장문'),
        ('CHOICE', '객관식 단일'),
        ('MULTIPLE', '객관식 복수'),
        ('SCALE', '척도 1-5'),
    ]
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='설문',
    )
    text = models.CharField(max_length=500, verbose_name='질문 내용')
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        verbose_name='질문 유형',
    )
    required = models.BooleanField(default=True, verbose_name='필수 여부')
    options = models.JSONField(default=list, blank=True, verbose_name='선택지')
    order = models.PositiveIntegerField(default=0, verbose_name='순서')

    class Meta:
        ordering = ['order']
        verbose_name = '질문'
        verbose_name_plural = '질문 목록'

    def __str__(self):
        return f'[{self.survey.title}] {self.text[:50]}'


class Response(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='설문',
    )
    respondent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='survey_responses',
        verbose_name='응답자',
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='제출일')

    class Meta:
        unique_together = ('survey', 'respondent')
        verbose_name = '응답'
        verbose_name_plural = '응답 목록'

    def __str__(self):
        return f'{self.survey.title} - {self.respondent}'


class Answer(models.Model):
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='응답',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='질문',
    )
    answer_text = models.TextField(blank=True, verbose_name='답변')

    class Meta:
        verbose_name = '답변'
        verbose_name_plural = '답변 목록'

    def __str__(self):
        return f'{self.question.text[:30]}: {self.answer_text[:30]}'
