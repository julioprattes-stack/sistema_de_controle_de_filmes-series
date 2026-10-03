from django.forms import ModelForm
from tracking import models

class RegisterTrackingForm(ModelForm):
    class Meta:
        model = models.WatchEntryModel
        fields = '__all__'