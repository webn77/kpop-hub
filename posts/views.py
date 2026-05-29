from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import CommentForm, PostForm
from .models import Comment, Like, Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('likes', 'comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from notices.models import Notice
        context['pinned_notices'] = Notice.objects.filter(is_pinned=True)[:3]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(view_count=F('view_count') + 1)
        obj.refresh_from_db(fields=['view_count'])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        ctx['comments'] = self.object.comments.select_related('author')
        if self.request.user.is_authenticated:
            ctx['user_liked'] = Like.objects.filter(
                user=self.request.user, post=self.object
            ).exists()
        else:
            ctx['user_liked'] = False
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, '본인의 게시글만 수정할 수 있습니다.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:list')

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, '본인의 게시글만 삭제할 수 있습니다.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class PostLikeView(LoginRequiredMixin, View):
    """HTMX POST — 좋아요 토글, _like_button.html partial 반환."""

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            user_liked = False
        else:
            user_liked = True
        html = render_to_string(
            'posts/_like_button.html',
            {'post': post, 'user_liked': user_liked},
            request=request,
        )
        return HttpResponse(html)


class CommentCreateView(LoginRequiredMixin, View):
    """HTMX POST — 댓글/대댓글 작성, _comment_tree.html partial 반환."""

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = form.cleaned_data.get('parent_id')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(pk=parent_id)
                except Comment.DoesNotExist:
                    comment.parent = None
            comment.save()
        comments = post.comments.select_related('author')
        html = render_to_string(
            'posts/_comment_tree.html',
            {'comments': comments, 'post': post},
            request=request,
        )
        return HttpResponse(html)


class CommentDeleteView(LoginRequiredMixin, View):
    """댓글 삭제 — 작성자 본인만."""

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author != request.user:
            return HttpResponse(
                '<p class="text-red-500 text-sm px-4 py-2">본인의 댓글만 삭제할 수 있습니다.</p>',
                status=403,
            )
        post = comment.post
        comment.delete()
        comments = post.comments.select_related('author')
        html = render_to_string(
            'posts/_comment_tree.html',
            {'comments': comments, 'post': post},
            request=request,
        )
        return HttpResponse(html)
