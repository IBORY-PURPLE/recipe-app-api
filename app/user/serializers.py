"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers


# serializer의 역할
# 1. 역직렬화 : == request로 생각해서 json 객체를 파이썬 객체로 바꿔서 db에 저장.
# 2. 직렬화 : ==response로 생각해서 db에서 클라이언트로 (파이썬 객체 -> json 객체)
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    # serializer가 지정한 모델을 인식하기 위한 설정
    class Meta:
        model = get_user_model()
        # 이 필드에 설정된 필드만 시리얼라이저에게 전달되서 유효성 검사를 진행한다.
        fields = ['email', 'password', 'name']
        # 비밀번호에 대한 추가설정을 놓는 변수
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # 만약 serializer로 통과되면 유저를 생성하는 함수
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        # super는 부모 클래스가 상속받은 클래스의 하위 함수를 쓰기위함
        # 여기서는 ModelSerializer안의 update()함수를 사용하기 위함 여기서
        # UserSerializer의 update와는 다른 update함수라는 점.
        # 이 update는 password를 제외한 나머지 값을 업데이트하고 if문에서
        # password는 해쉬값으로 설정하고 저장한다.
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    # serializer.is_vail()를 호출하면 이 함수가 호출됨.
    # attrs 값으로 유저가 post한 email과 password값이 들어오겠네?
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        # authenticate함수는 유저 인증을 확인하는 함수인가? 맞다면 어디 클래스 안에 정의되어있어?
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
