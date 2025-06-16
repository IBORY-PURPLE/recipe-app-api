"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

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
        fields = ['email','password', 'name']
        # 비밀번호에 대한 추가설정을 놓는 변수
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # 만약 serializer로 통과되면 유저를 생성하는 함수
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)