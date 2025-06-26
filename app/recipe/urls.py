"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# router.register는 recipe디렉토리 하위 url경로를 자동으로 만드는 것이고 그 url을
# urlpatterns에 넣어서 접근을 허용해준다.
# views.RecipeViewSet은 각 url마다 어떤 동작을 할지 정해주는 핵심 로직 클래스
# viewset은 url와 db모델 사이의 컨트롤러 역할을 하는 클래스라고 보자.
router.register('recipe', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
