from datetime import date
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from tracking.models import WatchEntryModel

class RegisterTrackingForm(ModelForm):
    class Meta:
        model = WatchEntryModel
        fields = ["title", "status", "rating", "current_season",
                  "current_episode", "finished_on", "comment"]

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if self.instance.pk:                      # edição: não troca o título
            del self.fields["title"]

    def clean(self):
        data = super().clean()
        title = data.get("title") or self.instance.title if self.instance.pk else data.get("title")

        if not self.instance.pk and self.user and title:
            if WatchEntryModel.objects.filter(user=self.user, title=title).exists():
                raise ValidationError("Este título já está na sua lista.")

        if title and title.type == "movie" and (data.get("current_season") or data.get("current_episode")):
            raise ValidationError("Temporada e episódio só valem para séries.")

        if data.get("status") == "done" and not data.get("finished_on"):
            data["finished_on"] = date.today()
        return data