from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from .models import User, Follow
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class SignUpSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)
    phone_number = serializers.CharField(max_length=17)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', "phone_number"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError('The Email has alreaday been Used')

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user


class CurrentUserPostSerializer(serializers.ModelSerializer):
    Posts = serializers.HyperlinkedIdentityField(
        many=True,
        view_name='post_by_id',
        queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'Posts']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower']


class Logoutserializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):

        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError('bad_token')
