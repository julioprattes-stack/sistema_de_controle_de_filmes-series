from django.forms import ModelForm
from catalog import models

class RegisterTitleForm(ModelForm):
    class Meta:
        model = models.TitleModel
        fields = '__all__'