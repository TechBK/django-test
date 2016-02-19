from rest_framework import serializers
from django.contrib.auth.models import User
from .models import NoteText, Tag, Note


class UserSerializer(serializers.ModelSerializer):
    # password1 = serializers.CharField(write_only=True)
    # password2 = serializers.CharField(write_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='notes:users-detail',
        lookup_field='username',
    )
    notes_url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-of-user',
        lookup_field='username',
        lookup_url_kwarg='username',
    )

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'is_superuser', 'password',
                   'user_permissions')
        depth = 1
        read_only_fields = ('last_login', 'date_joined', 'username',)


    # def create(self, validated_data):
    #     raise NotImplementedError('`create()` must be implemented.')
        # return User.objects.create(username=validated_data['username'],
        #                            password=validated_data['password1'])

    def save(self, **kwargs):
        raise NotImplementedError('`save()` must be implemented.')


class TextSplitWriteOnlyField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['write_only'] = True
        super(TextSplitWriteOnlyField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        if not data:
            return []
        return data.split(',')

class NoteTextSerializer(serializers.ModelSerializer):
    note_url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-detail',
        source='note.id',
    )

    class Meta:
        model = NoteText
        exclude = ('note',)
        # fields = ('')


class NoteTextSlugSerializer(serializers.ModelSerializer):
    # note_url = serializers.HyperlinkedIdentityField(
    #     view_name='notes:notes-detail',
    #     source='note.id',
    # )

    class Meta:
        model = NoteText
        fields = ('position', 'text')
        read_only_fields = ('position',)


class TagSerializer(serializers.ModelSerializer):
    notes_url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-of-tag',
        lookup_field='name',
    )

    class Meta:
        model = Tag


class UserSlugSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class NoteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-detail',
        # source='id'
    )

    users = serializers.SlugRelatedField(many=True,
                                         # queryset=User.objects.all(),
                                         read_only=True,
                                         slug_field='username',
                                         )
    # usernames = serializers.ListField(many=T)
    # text =
    notetext_set = NoteTextSerializer(many=True)

    tag_names = serializers.ListField(child=serializers.CharField(), write_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        # queryset=Tag.objects.all(),
        read_only=True,
        slug_field='name',
        required=False
    )

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('time', )
        extra_kwargs = {'is_public': {'required': False},
                        'is_deleted': {'required': False}
                        }


    def create(self, validated_data):
        request = self.context.get('request', None)
        assert request is not None, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )

        notetext_set_data = validated_data.pop('notetext_set')
        assert notetext_set_data is not None, \
        serializers.ValidationError({'notetext_set':'`notetext_set` is required'})

        users_data = validated_data.pop('users')

        # if users_data:
        # users = [ User.objects.get(user=u) for u in users_data]
        # users = [ User.objects.get(username=u) for u in users_data]
        if request.user not in users_data:
            users_data.append(request.user)
        note = Note.objects.create()
        note.users.add(*users_data)
        note.save()



        for pos, notetext in enumerate(notetext_set_data):
            NoteText.objects.create(position=pos, note=note, **notetext)
        # note.notetext_set.create(text=validated_data['text'], position=0)
        for tag_name in validated_data.get('tag_names'):
            tag, created = Tag.objects.get_or_create(name=tag_name)
            note.tags.add(tag)
        return note.save()


