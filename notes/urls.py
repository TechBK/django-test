from django.conf.urls import url
from .views import NotesView

app_name = 'notes'

urlpatterns = [
    url(r'', NotesView.as_view(), name='index'),
]
