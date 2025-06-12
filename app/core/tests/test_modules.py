"""
user model을 테스트한다.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Testing the created user model succesfully.
        objects는 장고 모델 클래스 안에 있는 메니저객체로서
        DB에 있는 유저를 가져오거나 DB에 새로운 유저를 만들수 있음."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
