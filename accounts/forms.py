from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with email verification."""
    
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
    )
    username_display = forms.CharField(
        label=_("Username"),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    
    class Meta:
        model = User
        fields = ('email', 'username_display', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email
    
    def clean_username_display(self):
        username_display = self.cleaned_data.get('username_display')
        if User.objects.filter(username_display=username_display).exists():
            raise ValidationError(_("A user with that username already exists."))
        return username_display


class UserLoginForm(AuthenticationForm):
    """Form for user login."""
    
    username = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )
    
    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive. Please verify your email."),
    }


class EmailVerificationForm(forms.Form):
    """Form for email verification."""
    
    token = forms.CharField(
        label=_("Verification Token"),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_token(self):
        token = self.cleaned_data.get('token')
        if not self.user or token != self.user.email_verification_token:
            raise ValidationError(_("Invalid verification token."))
        return token


class CharacterCreationForm(forms.Form):
    """Form for character creation."""
    
    CHARACTER_CHOICES = [
        ('criminal', 'Criminal'),
        ('police', 'Police Officer'),
    ]
    
    character_type = forms.ChoiceField(
        label=_("Character Type"),
        choices=CHARACTER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )