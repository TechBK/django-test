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
    template_name = 'notes/test.html'

    def get_query(self):
        """
        Cho nay chua toi uu phan truy van notes
        :return: QuerySet - danh sach note cua nguoi dung
        """
        # BUG?: users=self.request.user co dung ko?
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
                note.tags.add(tag)
            note.save()
            return redirect('notes:index')
        # data = noteform.errors
        data = {"post": request.POST, "error_messages": noteform.errors}
        return JsonResponse(data, safe=False)


class PublicNoteView(generic.TemplateView):
    """
    Xem public note cua nguoi khac.
    """
    template_name = 'notes/public_notes.html'

    def __init__(self):
        pass
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
        return JsonResponse({'errors':True, 'error_messages':'Note da co trong reponse cua ban!'})


############################################################
from django.contrib.auth import forms as auth_forms
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import Http404
from .serializers import UserSerializer, NoteTextSerializer, NoteSerializer, TagSerializer
from rest_framework import status

class UserListApi(APIView):
    """
    /users/
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users,
                                    many=True,
                                    context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     user = User.objects.create(**serializer.validated_data)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        form = auth_forms.UserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailApi(APIView):
    """
    users-detail
    /users/`username`/
    """
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username=username)
        serializer = UserSerializer(user,
                                    context={'request': request})
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_object(username)
        request.data['username'] = request.data.pop('username', username)
        request.data['date_joined'] = request.data.pop('date_joined', user.date_joined)
        form = auth_forms.UserChangeForm(request.data, instance=user)
        if form.is_valid():
            user = form.save()
            serializer = UserSerializer(user)
        # if serializer.is_valid():
        #     User.objects.filter(username=username).update(**serializer.validated_data)
            return Response(serializer.data)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, username, format=None):
        user = self.get_object(username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class NotesListApi(APIView):
    """
    notes:notes
    notes/
    """

    def get(self, request, format=None):
        notes = Note.objects.get(user=request.user)
        serializer = NoteSerializer(notes,
                                    many=True,
                                    context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data,
                                    context={'request':request})
        if serializer.is_valid():
            # note = Note.objects.create(**serializer.validated_data)
            # note.users.add(request.user)
            # note.save()
            # _serializer = NoteSerializer(note)
            note = serializer.save()
            return Response(serializer.data)


class NotesOfUserApi(APIView):
    """
    notes:notes_of_user
    /notes/`username`/
    """
    def get(self, request, username, format=None):
        notes = Note.objects.filter(users__username=username)
        serializer = NoteSerializer(notes,
                                    many=True,
                                    context={'request': request})
        return Response(serializer.data)

    def post(self, request, username, format=None):
        serializer = NoteSerializer(data=request.data, context={'request': request})
        # return Response(request.data)
        if serializer.is_valid():
            # serializer.save()
            # Note.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotesOfTagApi(APIView):
    """
    notes:notes_of_tag
    /tags/`tagname`/
    """
    def get(self, request, name, format=None):
        notes = Note.objects.filter(tags__name=name)
        serializer = NoteSerializer(notes,
                                    many=True,
                                    context={'request': request})
        return Response(serializer.data)


class NoteDetailApi(APIView):
    """
    /notes/`pk`/
    """
    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note,
                                    context={'request': request})
        return Response(serializer.data)


class TagsOfNoteApi(APIView):
    """
    /notes/`note_pk`/tags/
    """
    def get(self, request, note_pk):
        tags = Tag.objects.filter(notes__pk=note_pk)
        serializer = TagSerializer(tags,
                                   many=True,
                                   context={'request': request})
        return Response(serializer.data)


class TagListApi(APIView):
    """
    /tags/
    """
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags,
                                   many=True,
                                   context={'request': request})
        return Response(serializer.data)

