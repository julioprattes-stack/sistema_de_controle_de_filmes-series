from django.contrib import admin
from .models import GenusModel, PlatformModel, TitleModel

admin.site.register(GenusModel)
admin.site.register(PlatformModel)
admin.site.register(TitleModel)
