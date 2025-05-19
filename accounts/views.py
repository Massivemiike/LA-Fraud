import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from .forms import UserRegistrationForm, UserLoginForm, EmailVerificationForm, CharacterCreationForm
from .models import User, Profile


def register(request):
    """View for user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            
            # Generate verification token
            token = str(uuid.uuid4())
            user.email_verification_token = token
            
            # Save user
            user.save()
            
            # Send verification email
            subject = 'Verify your email address'
            html_message = render_to_string('accounts/email/verification_email.html', {
                'user': user,
                'token': token,
                'verification_url': request.build_absolute_uri(
                    reverse('verify_email', kwargs={'user_id': user.id})
                ),
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email
            
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Registration successful. Please check your email to verify your account.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, user_id):
    """View for email verification."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user ID.')
        return redirect('login')
    
    if user.is_email_verified:
        messages.info(request, 'Your email is already verified. Please log in.')
        return redirect('login')
    
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST, user=user)
        if form.is_valid():
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            
            # Create profile for the user
            Profile.objects.create(user=user)
            
            messages.success(request, 'Email verification successful. You can now log in.')
            return redirect('character_creation', user_id=user.id)
    else:
        form = EmailVerificationForm(user=user)
    
    return render(request, 'accounts/verify_email.html', {'form': form, 'user': user})


def user_login(request):
    """View for user login."""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.is_email_verified:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username_display}!')
                    return redirect('game_home')
                else:
                    messages.error(request, 'Please verify your email before logging in.')
                    return redirect('verify_email', user_id=user.id)
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def character_creation(request, user_id):
    """View for character creation."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user ID.')
        return redirect('login')
    
    # Ensure the user is the current logged-in user
    if request.user != user:
        messages.error(request, 'You do not have permission to create a character for this user.')
        return redirect('login')
    
    # Check if the user already has a profile with a character type
    try:
        profile = user.profile
        if profile.character_type:
            messages.info(request, 'You already have a character. Redirecting to the game.')
            return redirect('game_home')
    except Profile.DoesNotExist:
        # Create a profile if it doesn't exist
        profile = Profile.objects.create(user=user)
    
    if request.method == 'POST':
        form = CharacterCreationForm(request.POST)
        if form.is_valid():
            character_type = form.cleaned_data.get('character_type')
            profile.character_type = character_type
            profile.save()
            
            messages.success(request, f'Your {profile.get_character_type_display()} character has been created!')
            return redirect('game_home')
    else:
        form = CharacterCreationForm()
    
    return render(request, 'accounts/character_creation.html', {'form': form, 'user': user})


@login_required
def profile_view(request):
    """View for user profile."""
    user = request.user
    profile = user.profile
    
    return render(request, 'accounts/profile.html', {'user': user, 'profile': profile})