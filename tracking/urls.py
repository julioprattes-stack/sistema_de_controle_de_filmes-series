from django.urls import path
from tracking import views

app_name = 'tracking'

urlpatterns = [
    path("", views.WatchEntryListView.as_view(), name="entry_list"),
    path("new/", views.WatchEntryCreateView.as_view(), name="entry_create"),
    path("<int:pk>/update/", views.WatchEntryUpdateView.as_view(), name="entry_update"),
    path("<int:pk>/delete/", views.WatchEntryDeleteView.as_view(), name="entry_delete"),
]
