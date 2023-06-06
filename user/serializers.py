"""
Serializers for user Api View
"""

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer, Serializer, \
    EmailField, CharField, ValidationError


class UserSerializer(ModelSerializer):
    """Serializers for the User Object"""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {'password': {'write_only': True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # User can not change mail address because that is primary key
        validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class TokenSerializer(Serializer):
    username = EmailField(label="Username", write_only=True)
    password = CharField(label="Password", style={'input_type': 'password'},
                         trim_whitespace=True, write_only=True)
    token = CharField(label="Token", read_only=True)

    def create(self, validated_data):
        user = validated_data.pop('user')
        return Token.objects.get_or_create(user=user)[0]

    def to_representation(self, instance: Token):
        representation = super().to_representation(instance)
        representation['token'] = instance.key
        return representation

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)
        if not user:
            msg = _('Unable To Authenticate With Provided Credentials')
            raise ValidationError(detail=msg, code="authorization")
        attrs['user'] = user
        return attrs
