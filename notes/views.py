from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic
from .forms import NoteForm
from .models import Note, Tag


class NotesView(LoginRequiredMixin, generic.TemplateView):
    """
    LoginRequiredMixin class require LogIn
    """
    login_url = '/login/'
    template_name = 'notes/index.html'

    def get_query(self):
        """
        Cho nay chua toi uu phan truy van notes
        :return:
        """
        notes = Note.objects.filter(users=self.request.user)
        return notes

    def get_context_data(self, **kwargs):
        context = super(NotesView, self).get_context_data(**kwargs)
        context['notes'] = self.get_query()
        return context

    def post(self, request, *args, **kwargs):
        noteform = NoteForm(request.POST)
        if noteform.is_valid():
            note = Note.objects.create()
            note.users.add(request.user)
            note.save()
            note.notetext_set.create(text=noteform.cleaned_data['text'], position=0)
            for tag_name in noteform.cleaned_data['tags']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # tag.note_set.add(note)
                # tag.save()
                note.tags.add(tag)
                note.save()

            # tags = [Tag.objects.get_or_create(name=str(tag_name)) for tag_name in noteform.cleaned_data['tags']]
            # note.tags.set(tags)
            # for tag_name in noteform.cleaned_data['tags']
            # note.tags.get_or_create(name=tag_name)
        return redirect('notes:index')
