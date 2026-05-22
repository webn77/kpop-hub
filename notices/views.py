from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Notice


class StaffRequiredMixin(UserPassesTestMixin):
    """staff 또는 ADMIN 역할 사용자만 접근 허용."""

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_staff or getattr(user, 'role', '') == 'ADMIN'
        )

    def handle_no_permission(self):
        messages.error(self.request, '관리자만 접근할 수 있는 페이지입니다.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class NoticeListView(ListView):
    model = Notice
    template_name = 'notices/list.html'
    context_object_name = 'notices'
    paginate_by = 10

    def get_queryset(self):
        return Notice.objects.select_related('author').all()


class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'notices/detail.html'
    context_object_name = 'notice'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # 조회수 증가 (비동기 경쟁 없이 F() 사용)
        from django.db.models import F
        Notice.objects.filter(pk=obj.pk).update(view_count=F('view_count') + 1)
        obj.refresh_from_db(fields=['view_count'])
        return obj


class NoticeCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Notice
    template_name = 'notices/form.html'
    fields = ['title', 'content', 'is_pinned']
    success_url = reverse_lazy('notices:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '공지사항이 등록되었습니다.')
        return super().form_valid(form)


class NoticeUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Notice
    template_name = 'notices/form.html'
    fields = ['title', 'content', 'is_pinned']

    def get_success_url(self):
        return reverse_lazy('notices:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, '공지사항이 수정되었습니다.')
        return super().form_valid(form)


class NoticeDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Notice
    template_name = 'notices/confirm_delete.html'
    success_url = reverse_lazy('notices:list')

    def form_valid(self, form):
        messages.success(self.request, '공지사항이 삭제되었습니다.')
        return super().form_valid(form)
