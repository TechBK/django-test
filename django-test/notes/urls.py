from django.conf.urls import url
from .views import NotesView, \
    PublicNoteView, \
    AddNoteView, \
    UserListApi, \
    UserDetailApi, \
    NoteDetailApi, \
    NoteListApi


app_name = 'notes'

urlpatterns = [
    url(r'^public/$', PublicNoteView.as_view(), name='public'),
    url(r'^add/$', AddNoteView.as_view(), name='add'),
    url(r'^$', NotesView.as_view(), name='index'),
    url(r'^users/$', UserListApi.as_view(), name='users'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetailApi.as_view(), name='users-detail'),
    url(r'^(?P<pk>[0-9]+)/notes/$', NoteListApi.as_view(), name='notes'),
    url(r'^notes/(?P<pk>[0-9]+)/$', NoteDetailApi.as_view(), name='notes-detail')
]
