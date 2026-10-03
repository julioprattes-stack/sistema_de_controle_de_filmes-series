from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncMonth
from django.views.generic import TemplateView

from catalog.models import TitleModel
from tracking.models import WatchEntryModel



class StatsView(LoginRequiredMixin, TemplateView):
    template_name = "stats/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entries = WatchEntryModel.objects.filter(user=self.request.user)
        done = entries.filter(status=WatchEntryModel.Status.DONE)

        # Cartões de resumo
        context["summary"] = entries.aggregate(
            total=Count("id"),
            done=Count("id", filter=Q(status=WatchEntryModel.Status.DONE)),
            watching=Count("id", filter=Q(status=WatchEntryModel.Status.WATCHING)),
            planned=Count("id", filter=Q(status=WatchEntryModel.Status.PLANNED)),
            dropped=Count("id", filter=Q(status=WatchEntryModel.Status.DROPPED)),
            avg_rating=Avg("rating", filter=Q(status=WatchEntryModel.Status.DONE)),
        )

        # Filmes x séries assistidos
        kind_labels = dict(TitleModel.Type.choices)
        by_kind = done.values("title__type").annotate(total=Count("id"))
        kind_data = {
            "labels": [kind_labels[row["title__type"]] for row in by_kind],
            "values": [row["total"] for row in by_kind],
        }

        # Gêneros mais vistos, com nota média
        by_genre = (
            done.filter(title__genres__isnull=False)
            .values("title__genres__name")
            .annotate(total=Count("id"), avg=Avg("rating"))
            .order_by("-total")[:8]
        )
        genre_data = {
            "labels": [row["title__genres__name"] for row in by_genre],
            "values": [row["total"] for row in by_genre],
            "ratings": [
                round(row["avg"], 1) if row["avg"] is not None else None
                for row in by_genre
            ],
        }

        # Assistidos por mês (últimos 12 meses com registro)
        by_month = list(
            done.filter(finished_on__isnull=False)
            .annotate(month=TruncMonth("finished_on"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )[-12:]
        month_data = {
            "labels": [row["month"].strftime("%m/%Y") for row in by_month],
            "values": [row["total"] for row in by_month],
        }

        context["chart_data"] = {
            "kind": kind_data,
            "genre": genre_data,
            "month": month_data,
        }
        return context
