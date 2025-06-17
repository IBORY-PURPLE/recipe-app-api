"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

# CREATE_USER_URL = reverse('user:create') test코드에 있는
# 이 라인때문에 app 이름을 설정해준다는데 굳이 할 필요있나?
# reverse('앱 네임스페이스:~') 앱 네임스페이스를 사용했을 경우 user앱의
# urls파일에 앱 네임이 명시되어있어야 저 코드가 실행된다고 한다.
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]