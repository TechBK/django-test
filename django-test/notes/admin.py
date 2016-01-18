from django.contrib import admin

from .models import Note, Tag, NoteText

admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(NoteText)