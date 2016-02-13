from django.conf.urls import url
from .views import NotesView, \
    PublicNoteView, \
    AddNoteView, \
    UserListApi, \
    UserDetailApi, \
    NoteDetailApi, \
    NotesOfUserApi, \
    TagsOfNoteApi, \
    TagListApi


app_name = 'notes'

urlpatterns = [
    url(r'^public/$',
        PublicNoteView.as_view(),
        name='public'),
    url(r'^add/$',
        AddNoteView.as_view(),
        name='add'),
    url(r'^$',
        NotesView.as_view(),
        name='index'),
    url(r'^users/$',
        UserListApi.as_view(),
        name='users'),
    url(r'^users/(?P<username>\D+)/$',
        UserDetailApi.as_view(),
        name='users-detail'),
    url(r'^(?P<username>\D+)/notes/$',
        NotesOfUserApi.as_view(),
        name='notes'),
    url(r'^notes/(?P<pk>[0-9]+)/$',
        NoteDetailApi.as_view(),
        name='notes-detail'),
    url(r'^notes/(?P<note_pk>[0-9]+)/tags/$',
        TagsOfNoteApi.as_view(),
        name='tags-of-note'),
    url(r'^tags/$',
        TagListApi.as_view(),
        name='tags'
        )
]
