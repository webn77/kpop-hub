from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Like, Post

User = get_user_model()


class PostListPaginationTest(TestCase):
    """test_post_list_paginates_15: 첫 페이지에 게시글 15개."""

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass', nickname='user1')
        for i in range(16):
            Post.objects.create(
                author=self.user,
                title=f'Post {i}',
                content='content',
            )

    def test_post_list_paginates_15(self):
        response = self.client.get(reverse('posts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 15)


class LikeToggleTest(TestCase):
    """test_like_toggle: 좋아요 POST → 생성, 재POST → 삭제."""

    def setUp(self):
        self.user = User.objects.create_user(username='liker', password='pass', nickname='liker')
        self.post = Post.objects.create(
            author=self.user,
            title='Like Test',
            content='content',
        )
        self.url = reverse('posts:like', kwargs={'pk': self.post.pk})

    def test_like_toggle(self):
        self.client.login(username='liker', password='pass')
        # 첫 번째 POST → 좋아요 생성
        self.client.post(self.url)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())
        # 두 번째 POST → 좋아요 삭제
        self.client.post(self.url)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())


class CommentCreateLoginTest(TestCase):
    """test_comment_create_requires_login: 미로그인 댓글 POST → 302."""

    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='pass', nickname='owner_comment')
        self.post = Post.objects.create(
            author=self.user,
            title='Comment Test',
            content='content',
        )
        self.url = reverse('posts:comment_create', kwargs={'pk': self.post.pk})

    def test_comment_create_requires_login(self):
        response = self.client.post(self.url, {'content': 'hello'})
        self.assertEqual(response.status_code, 302)


class CommentDeleteTest(TestCase):
    """댓글 삭제 권한 테스트."""

    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass', nickname='owner_del')
        self.other = User.objects.create_user(username='other', password='pass', nickname='other_del')
        self.post = Post.objects.create(
            author=self.owner,
            title='Delete Test',
            content='content',
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.owner,
            content='test comment',
        )
        self.url = reverse('posts:comment_delete', kwargs={'pk': self.comment.pk})

    def test_comment_delete_by_owner_succeeds(self):
        self.client.login(username='owner', password='pass')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_comment_delete_by_other_user_returns_403(self):
        self.client.login(username='other', password='pass')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())
