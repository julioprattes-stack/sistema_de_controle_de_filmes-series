from django.db import models
from django.conf import settings

class WatchEntryModel(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Quero ver"
        WATCHING = "watching", "Assistindo"
        DONE = "done", "Assistido"
        DROPPED = "dropped", "Abandonado"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.ForeignKey("catalog.TitleModel", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PLANNED)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    current_season = models.PositiveSmallIntegerField(null=True, blank=True)
    current_episode = models.PositiveSmallIntegerField(null=True, blank=True)
    finished_on = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="one_entry_per_user_title"),
            models.CheckConstraint(
                condition=models.Q(rating__isnull=True) | models.Q(rating__gte=1, rating__lte=10),
                name="rating_between_1_and_10",
            ),
        ]