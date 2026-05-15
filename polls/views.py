from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.db import IntegrityError

from .models import Poll, PollChoice, PollVote


class PollListView(ListView):
    model = Poll
    template_name = 'polls/list.html'
    context_object_name = 'polls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_polls = Poll.objects.select_related('created_by').all()
        context['active_polls'] = [p for p in all_polls if p.is_active]
        context['ended_polls'] = [p for p in all_polls if not p.is_active]
        context['tab'] = self.request.GET.get('tab', 'active')
        return context


class PollDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        user_voted = PollVote.objects.filter(
            user=request.user,
            choice__poll=poll
        ).exists()
        # 종료된 투표 or 이미 투표한 경우 결과 표시
        show_result = not poll.is_active or user_voted
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'show_result': show_result,
            'user_voted': user_voted,
        })


class PollVoteView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)

        if not poll.is_active:
            messages.error(request, '종료된 투표입니다.')
            return redirect('polls:result', pk=pk)

        # 이미 투표했는지 확인
        already_voted = PollVote.objects.filter(
            user=request.user,
            choice__poll=poll
        ).exists()
        if already_voted:
            messages.warning(request, '이미 투표하셨습니다.')
            return redirect('polls:result', pk=pk)

        # 선택 항목 수집 (단일/복수)
        if poll.is_multiple:
            choice_ids = request.POST.getlist('choices')
        else:
            choice_id = request.POST.get('choice')
            choice_ids = [choice_id] if choice_id else []

        if not choice_ids:
            messages.error(request, '항목을 선택해 주세요.')
            return redirect('polls:detail', pk=pk)

        # 투표 저장 (IntegrityError는 중복 방지용 fallback)
        try:
            for cid in choice_ids:
                choice = get_object_or_404(PollChoice, pk=cid, poll=poll)
                PollVote.objects.create(user=request.user, choice=choice)
        except IntegrityError:
            messages.error(request, '중복 투표는 허용되지 않습니다.')
            return redirect('polls:detail', pk=pk)

        messages.success(request, '투표가 완료되었습니다.')
        return redirect('polls:result', pk=pk)


class PollResultView(View):

    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        user_voted = (
            request.user.is_authenticated and
            PollVote.objects.filter(user=request.user, choice__poll=poll).exists()
        )
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'show_result': True,
            'user_voted': user_voted,
        })
