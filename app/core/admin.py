"""
django admin customizations
"""
from django.contrib import admin
# 기본 useradmin클래스와 내가 커스텀하는 useradmin클래스를 구분짓기 위해서 baseuseradmin으로 import해오는 것.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# _('Permission')이라는 섹션 제목을 번역하고 싶을 때 번역가능하게 해주는 함수
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pasges for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    # fieldsets 구조는 튜플의 연속으로 하나의 튜플은 user change페이지의 하나의 섹션으로 이해
    # (섹션 제목, {'feilds': ('필드1', '필드2', '필드3')}),
    # (
    #      센션 제목,
    #      {
    #           'feild': (
    #                 '필드1',
    #                 '필드2',
    #                 '필드3',
    #            )
    #      }
    # ),
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
