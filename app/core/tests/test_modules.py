"""
user model을 테스트한다.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

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

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe title',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description'
        )
        # str(recipe)가 Recipe모델 하위 함수인 str()호출해서 recipe.title을 가져오는거고
        # 두번째 인자인 recie.title은 test_create_recipe에서서 만들어진 'Sample recipe name'가져오니깐 당연히 두개가 같을 수 밖에 없는거아님?
        # 당연히 정답.
        self.assertEqual(str(recipe) , recipe.title)
