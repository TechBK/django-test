from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import redirect
from .forms import NoteForm
from .models import Note, Tag
from django.http import JsonResponse


class NotesView(LoginRequiredMixin, generic.TemplateView):
    """
    LoginRequiredMixin class require LogIn
    Ham get() da dinh nghia truoc nen khong can dinh nghia nua
    Ham get_context_data() de them context_data vao template
    """
    login_url = 'users:login'
    template_name = 'notes/index.html'

    def get_query(self):
        """
        Cho nay chua toi uu phan truy van notes
        :return: QuerySet - danh sach note cua nguoi dung
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
            note = Note.objects.create(is_public=noteform.cleaned_data['is_public'])
            note.users.add(request.user)
            note.save()
            note.notetext_set.create(text=noteform.cleaned_data['text'], position=0)
            for tag_name in noteform.cleaned_data['tags']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # tag.note_set.add(note)
                # tag.save()
                note.tags.add(tag)
            # Tag.objects.get_or_create(name='public',is_public)
            # note.tags.
            note.save()
            return redirect('notes:index')
            # tags = [Tag.objects.get_or_create(name=str(tag_name)) for tag_name in noteform.cleaned_data['tags']]
            # note.tags.set(tags)
            # for tag_name in noteform.cleaned_data['tags']
            # note.tags.get_or_create(name=tag_name)
        # data = noteform.errors
        data = [request.POST, noteform.errors]
        return JsonResponse(data, safe=False)


class PublicNoteView(generic.TemplateView):
    """
    Xem public note cua nguoi khac.
    """
    template_name = 'notes/public_notes.html'

    def get_query(self):
        """

        :return: List of public notes.
        """
        notes = Note.objects.filter(is_public=True)
        return notes

    def get_context_data(self, **kwargs):
        context = super(PublicNoteView, self).get_context_data(**kwargs)
        context['notes'] = self.get_query()
        return context


class AddNoteView(LoginRequiredMixin, generic.View):
    """
    add public note cua khac vao kho note cua minh
    """
    login_url = 'user:login'

    def post(self, request, *args, **kwargs):
        note_id = request.POST['note_id']
        note = Note.objects.get(pk=note_id)
        if request.user not in note.users.all():
            note.pk = None
            note.save()
            note.users.set([request.user, ])
            note.save()
            old_note = Note.objects.get(pk=note_id)
            # full clone notetext
            for notetext in old_note.notetext_set.all():
                notetext.pk = None
                notetext.save()
                note.notetext_set.add(notetext)
            # clone tag
            note.tags.set(old_note.tags.all())
            note.save()

            return redirect('notes:index')
        return JsonResponse({'errors':'da co san roi nhe'})
