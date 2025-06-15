"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# api/user/create
CREATE_USER_URL = reverse('user:create')

def create_user(**user_data):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**user_data)


class PublicUserApiTest(TestCase):
    """Test teh public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        # javascript로 유저 데이터를 json형식으로 읽어오는 데이터를 칭함.
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # payload에 있는 데이터가 해당 URL로 post되어지는 원리
        # URL이 브라우저 주소창도 있지만 django앱도 url로 매핑되어있는 원리.
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # email이 payload에 있는 email값이 같은 user을 db에서 가져와서 유저를 생성한다는 건가?그리고 password 체크하고?
        # 정확히 보면 이미 .post()로 유저는 생성이 되었고 유저가 생성이 잘 되었는지 get과 password확인으로 점검하는 코드이다.
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    # 이미 가입이 완료된 유저가 같은 이메일로 재가입을 시도할 때 적절한 오류가 나오는지 테스트하는 함수
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # 테스트를 위해 인위적으로 유저 생성.
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # 비밀번호가 짧은 유저가 실제로 db에 저장되어 있지 않은지 확인하는 코드 결국 false값이 저장되어야함.
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)