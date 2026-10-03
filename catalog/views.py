from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from catalog.models import TitleModel
from catalog.forms import RegisterTitleForm

class TitleListView(ListView):
    model = TitleModel
    template_name = 'catalog/title_list.html'
    context_object_name = 'titles'
    paginate_by = 10

    def get(self):
        queryset = TitleModel.objects.prefetch_related('genres').order_by('name')
        search = self.request.GET.get('search')
        type = self.request.GET.get('type')
        if search:
            queryset = queryset.filter(name__icontains=search)
        if type:
            queryset = queryset.filter(type=type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = TitleModel.Type.choices
        return context

class TitleCreateView(LoginRequiredMixin, CreateView):
    model = TitleModel
    form_class = RegisterTitleForm
    template_name = 'catalog/title_form.html'
    success_url = reverse_lazy('catalog:title_list')

class TitleUpdateView(LoginRequiredMixin, UpdateView):
    model = TitleModel
    form_class = RegisterTitleForm
    template_name = 'catalog/title_form.html'
    success_url = reverse_lazy('catalog:title_list')
