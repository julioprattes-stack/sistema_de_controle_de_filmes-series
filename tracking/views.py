from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from catalog.models import GenusModel, TitleModel
from .models import WatchEntryModel
from .forms import RegisterTrackingForm

class OwnEntriesMixin(LoginRequiredMixin):
    """Restringe qualquer view aos registros do usuário logado."""

    def get_queryset(self):
        return WatchEntryModel.objects.filter(user=self.request.user).select_related(
            "title", "platform"
        )

class WatchEntryListView(OwnEntriesMixin, ListView):
    template_name = "tracking/entry_list.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-created_at")
        status = self.request.GET.get("status")
        kind = self.request.GET.get("kind")
        genre = self.request.GET.get("genre")
        search = self.request.GET.get("q")
        if status:
            queryset = queryset.filter(status=status)
        if kind:
            queryset = queryset.filter(title__kind=kind)
        if genre:
            queryset = queryset.filter(title__genres__id=genre)
        if search:
            search = search.filter(title__name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = WatchEntryModel.Status.choices
        context["kinds"] = TitleModel.Kind.choices
        context["genres"] = GenusModel.objects.order_by("name")
        return context
    
class WatchEntryCreateView(OwnEntriesMixin, CreateView):
    model = WatchEntryModel
    form_class = RegisterTrackingForm
    template_name = 'tracking/entry_form.html'
    success_url = reverse_lazy('tracking:entry_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WatchEntryUpadteView(OwnEntriesMixin, UpdateView):
    model = WatchEntryModel
    form_class = RegisterTrackingForm
    template_name = 'tracking/entry_form.html'
    success_url = reverse_lazy('tracking:entry_list')

class WatchEntryDeleteView(OwnEntriesMixin, DeleteView):
    model = WatchEntryModel
    success_url = reverse_lazy("tracking:entry_list")
