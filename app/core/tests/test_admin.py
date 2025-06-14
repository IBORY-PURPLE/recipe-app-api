"""
Test for the Django modificaion
"""
from django.test import TestCase
# get_user_model은 User클래스 그자체 models.User라 똑같이 클래스 그자체이다.
# setting.py에서 AUTH_USER_MODEL에 설정된 user model이 지정된다.
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for django admin"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='test123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='test123',
            name='Test User',
        )

    def test_users_lists(self):
        """Test that users are listed on page"""
        # core_useㅠr에 있는 userlist url을 저장하고
        url = reverse('admin:core_user_changelist')
        # 그 url에 있는 유저 정보를 get해와서 res변수에 저장?
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test te create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
