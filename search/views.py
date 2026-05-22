from django.views.generic import TemplateView
from django.db.models import Q
from notices.models import Notice
from posts.models import Post


class SearchView(TemplateView):
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        ctx['query'] = q
        if q:
            ctx['notices'] = Notice.objects.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )
            ctx['posts'] = Post.objects.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )
        else:
            ctx['notices'] = []
            ctx['posts'] = []
        return ctx
