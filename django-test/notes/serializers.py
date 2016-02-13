from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from django.contrib.auth import forms as auth_forms


class URLReadOnlyField(serializers.ReadOnlyField):
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
        source='*',
        read_only=True
    )
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    notes_url = serializers.HyperlinkedRelatedField(
        view_name='notes:notes',
        lookup_field='username',
        lookup_url_kwarg='username',
        source='*',
        read_only=True
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
    note = URLReadOnlyField(view_name='notes:notes-detail')
    text = serializers.CharField()
    position = serializers.IntegerField()


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    is_thread = serializers.BooleanField()


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    url = URLReadOnlyField(view_name='notes:notes-detail')
    content_type = serializers.CharField()
    time = serializers.DateTimeField()
    is_deleted = serializers.BooleanField(default=False)
    # tags_url = URLReadOnlyField(viewname='tag-of-note')
    # users = serializers.HyperlinkedRelatedField(view_name='notes:users-detail', queryset=User.objects.all())
    # users = URLReadOnlyField(view_name='notes:users-detail')
    # users = UserSerializer(many=True)
    users = serializers.SlugRelatedField(many=True,
                                         read_only=True,
                                         slug_field='username')
    is_public = serializers.BooleanField(default=False)
    # tags = TagWriteOnlyField()
    # content_url = URLReadOnlyField(viewname='content-of-note')
    notetext_set = NoteTextSerializer(many=True)
    # tags = TagSerializer(many=True)
    tags_nest = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source='tags')




