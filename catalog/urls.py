from django.urls import path
from catalog import views
app_name = 'catalog'

urlpatterns = [
    path('',views.TitleListView.as_view(), name='title_list'),
    path('new',views.TitleCreateView.as_view(), name='title_create'),
    path('<int:pk>/update',views.TitleUpdateView.as_view(), name='title_update'),
]
