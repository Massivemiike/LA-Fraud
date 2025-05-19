from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username_display')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Email verification'), {'fields': ('is_email_verified', 'email_verification_token')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username_display', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username_display', 'first_name', 'last_name', 'is_staff', 'is_email_verified')
    search_fields = ('email', 'username_display', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = (ProfileInline,)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin"""
    
    list_display = ('user', 'level', 'character_type', 'money', 'is_in_jail', 'is_in_hospital')
    list_filter = ('character_type', 'is_in_jail', 'is_in_hospital')
    search_fields = ('user__email', 'user__username_display')
    readonly_fields = ('user',)
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Character Type'), {'fields': ('character_type',)}),
        (_('Attributes'), {'fields': ('strength', 'speed', 'dexterity', 'defense')}),
        (_('Stats'), {'fields': ('level', 'experience', 'life', 'max_life', 'energy', 'max_energy', 
                                'endurance', 'max_endurance', 'mood', 'max_mood', 'knowledge_points')}),
        (_('Status'), {'fields': ('is_in_jail', 'jail_release_time', 'is_in_hospital', 'hospital_release_time')}),
        (_('Money'), {'fields': ('money', 'bank_money')}),
        (_('Location'), {'fields': ('current_location',)}),
    )