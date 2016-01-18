from django.conf.urls import url
from .views import NotesView, PublicNoteView, AddNoteView

app_name = 'notes'

urlpatterns = [
    url(r'^public/$', PublicNoteView.as_view(), name='public'),
    url(r'^add/$', AddNoteView.as_view(), name='add'),
    url(r'^$', NotesView.as_view(), name='index'),
]
