from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notices.models import Notice
from posts.models import Post

User = get_user_model()


class SearchTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='searcher', password='pass1234!')
        self.search_url = reverse('search:search')

    def test_search_returns_matching_posts(self):
        """게시글 생성 후 키워드 검색 → 결과 포함."""
        Post.objects.create(
            author=self.user,
            title='Django 튜토리얼',
            content='Django 웹 프레임워크 학습 내용',
        )
        response = self.client.get(self.search_url, {'q': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Django 튜토리얼', response.content.decode())

    def test_search_returns_matching_notices(self):
        """공지 생성 후 키워드 검색 → 결과 포함."""
        Notice.objects.create(
            author=self.user,
            title='중요 공지사항',
            content='Python 3.12 릴리즈 관련 공지',
        )
        response = self.client.get(self.search_url, {'q': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('중요 공지사항', response.content.decode())

    def test_search_empty_query_returns_empty(self):
        """q 없으면 결과 없음."""
        Post.objects.create(
            author=self.user,
            title='빈 검색 테스트',
            content='내용',
        )
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        ctx = response.context
        self.assertEqual(list(ctx['posts']), [])
        self.assertEqual(list(ctx['notices']), [])
