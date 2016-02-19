from django.conf.urls import url
from .views import NotesView, \
    PublicNoteView, \
    AddNoteView, \
    UserListApi, \
    UserDetailApi, \
    NoteDetailApi, \
    NotesOfUserApi, \
    TagsOfNoteApi, \
    TagListApi, \
    NotesOfTagApi


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

    url(r'^users/(?P<username>\w+)/$',
        UserDetailApi.as_view(),
        name='users-detail'),

    url(r'^notes/(?P<pk>[0-9]+)/$',
        NoteDetailApi.as_view(),
        name='notes-detail'),

    url(r'^notes/(?P<username>\w+)/$',
        NotesOfUserApi.as_view(),
        name='notes-of-user'),



    url(r'^notes/(?P<note_pk>[0-9]+)/tags/$',
        TagsOfNoteApi.as_view(),
        name='tags-of-note'),

    url(r'^tags/$',
        TagListApi.as_view(),
        name='tags'
        ),

    url(r'^tags/(?P<name>\D+)/$',
        NotesOfTagApi.as_view(),
        name='notes-of-tag'
        )
]
