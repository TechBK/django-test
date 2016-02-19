# from django.utils import timezone
from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.reverse import reverse
# from django.contrib.auth import forms as auth_forms


class URLReadOnlyField(serializers.ReadOnlyField):
    """
    Class nay ko dung :v :v
    """
    def __init__(self, **kwargs):
        self.view_name = kwargs.pop('view_name', None)
        assert self.view_name is not None, 'The `view_name` argument is required.'
        self.slug = kwargs.pop('slug', None)
        kwargs['source'] = '*'
        super(URLReadOnlyField, self).__init__(**kwargs)

    # doan nay da duoc thay the = kwargs['source'] = '*'
    # def get_attribute(self, instance):
    #     return instance

    def to_representation(self, value):
        """
        value = object
        :param value:
        :return:
        """
        request = self.context.get('request', None)
        assert request is not None, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )
        kwargs = {
            'pk':value.id
        }
        # return self.view_name
        # print(reverse(self.viewname, kwargs=kwargs, request=request))
        return reverse(self.view_name, kwargs=kwargs, request=request)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='notes:users-detail',
        lookup_field='username',
        lookup_url_kwarg='username',
        # source='username'
        # read_only=True # This field is always read-only.
    )
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    notes_url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-of-user',
        lookup_field='username',
        lookup_url_kwarg='username',
        # source='username'
        # read_only=True
    )
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()


class TagWriteOnlyField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['write_only'] = True
        super(TagWriteOnlyField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        if not data:
            return []
        return data.split(',')

class NoteTextSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    note_url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-detail',
        source='note.id',
    )
    text = serializers.CharField()
    position = serializers.IntegerField()


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    notes_url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-of-tag',
        lookup_field='name',
        lookup_url_kwarg='name',
        # source='name'
    )
    name = serializers.CharField()
    is_thread = serializers.BooleanField()


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='notes:notes-detail',
        # source='id'
    )
    content_type = serializers.CharField()
    time = serializers.DateTimeField()
    is_deleted = serializers.BooleanField(default=False)
    users = serializers.SlugRelatedField(many=True,
                                         read_only=True,
                                         slug_field='username')
    is_public = serializers.BooleanField(default=False)
    notetext_set = NoteTextSerializer(many=True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='tags'
    )

    def create(self, validated_data):
        """

        :param validated_data:
        :return:
        """

        note = Note.objects.create(**serializer.validated_data)
        note.users.add(request.user)
        note.save()




