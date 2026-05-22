from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notice

User = get_user_model()


class NoticeListAnonymousTest(TestCase):
    """test_notice_list_accessible_to_anonymous: 비로그인 목록 조회 → 200."""

    def test_notice_list_accessible_to_anonymous(self):
        response = self.client.get(reverse('notices:list'))
        self.assertEqual(response.status_code, 200)


class NoticeCreateStaffOnlyTest(TestCase):
    """test_notice_create_requires_staff: 일반 유저 작성 시도 → 리다이렉트 + 에러 메시지."""

    def setUp(self):
        self.normal_user = User.objects.create_user(
            username='normal', password='pass', nickname='normal_user'
        )

    def test_notice_create_requires_staff(self):
        self.client.login(username='normal', password='pass')
        response = self.client.get(reverse('notices:create'))
        # 403 대신 친절한 메시지와 함께 리다이렉트
        self.assertEqual(response.status_code, 302)
        # 메시지 확인
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('관리자' in str(m) for m in messages))


class NoticePinnedFirstTest(TestCase):
    """test_pinned_notice_appears_first: is_pinned=True 공지가 목록 첫 번째."""

    def setUp(self):
        self.staff = User.objects.create_user(
            username='staff', password='pass', is_staff=True, nickname='staff_user'
        )
        self.regular = Notice.objects.create(
            author=self.staff,
            title='일반 공지',
            content='내용',
            is_pinned=False,
        )
        self.pinned = Notice.objects.create(
            author=self.staff,
            title='중요 공지',
            content='중요 내용',
            is_pinned=True,
        )

    def test_pinned_notice_appears_first(self):
        response = self.client.get(reverse('notices:list'))
        self.assertEqual(response.status_code, 200)
        notices = list(response.context['notices'])
        self.assertEqual(notices[0].pk, self.pinned.pk)
