import calendar
from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Event
from .forms import EventForm


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_staff or getattr(user, 'role', '') == 'ADMIN'
        )

    def handle_no_permission(self):
        messages.error(self.request, '관리자만 일정을 관리할 수 있습니다.')
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class EventListView(ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        today = date.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        return Event.objects.filter(event_date__year=year, event_date__month=month).order_by('event_date')

    def _build_calendar(self, year, month, events_qs):
        """월 캘린더 딕셔너리 {day: [event, ...]} 반환."""
        cal = calendar.monthcalendar(year, month)
        event_map = {}
        for event in events_qs:
            event_map.setdefault(event.event_date.day, []).append(event)
        weeks = []
        for week in cal:
            week_data = []
            for day in week:
                week_data.append({
                    'day': day,
                    'events': event_map.get(day, []) if day != 0 else [],
                })
            weeks.append(week_data)
        return weeks

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))

        # 이전/다음 달 계산
        if month == 1:
            prev_year, prev_month = year - 1, 12
        else:
            prev_year, prev_month = year, month - 1
        if month == 12:
            next_year, next_month = year + 1, 1
        else:
            next_year, next_month = year, month + 1

        ctx.update({
            'year': year,
            'month': month,
            'month_name': f'{year}년 {month}월',
            'calendar_weeks': self._build_calendar(year, month, ctx['events']),
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'today': today,
        })
        return ctx


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'


class EventCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, '일정이 등록되었습니다.')
        return super().form_valid(form)
