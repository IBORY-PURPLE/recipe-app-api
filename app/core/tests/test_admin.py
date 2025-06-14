"""
Test for the Django modificaion
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for django admin"""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_user(
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
        # core_user에 있는 userlist url을 저장하고
        url = reverse('admin:core_user_changelist')
        # 그 url에 있는 유저 정보를 get해와서 res변수에 저장?
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
