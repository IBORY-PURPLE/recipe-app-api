"""
Tests for recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults ={
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'https://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unatuthenticated API requests."""

    def setUp(self):
        self.client =APIClient(self)

    def test_auth_required(self):
        """Test auth is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.ocm',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):
        "Test retriving a list of recipe."
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recip_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        # 두개의 recipe를 만드는데 recipe내용은 같고 유저만 다른 객체 두개가 생성되는거잖아 그치?
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        # 지금 setUp이 self.user로 로그인이 되어있는 상태다 보니까 self.user로 설정되어있는 recipe만 get하는 거잖아 그치?
        recipes = Recipe.objects.filter(user=self.user)
        serializer  = RecipeSerializer(recipes, many=True)
        # 잘 get됐는지 http상태 확인코드이고
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # res 할당된 data는 두개고 serializer.data는 로그인된 유저꺼 하나인데 true가 나오나?
        self.assertEqual(res.data, serializer.data)