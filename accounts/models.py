from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as the unique identifier."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    # Additional fields for player profile
    username_display = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username_display']

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Player profile with game-specific attributes."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Character attributes
    strength = models.IntegerField(default=10)
    speed = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    defense = models.IntegerField(default=10)
    
    # Character stats
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    life = models.IntegerField(default=100)
    max_life = models.IntegerField(default=100)
    energy = models.IntegerField(default=100)
    max_energy = models.IntegerField(default=100)
    endurance = models.IntegerField(default=100)
    max_endurance = models.IntegerField(default=100)
    mood = models.IntegerField(default=100)
    max_mood = models.IntegerField(default=100)
    knowledge_points = models.IntegerField(default=0)
    
    # Character status
    is_in_jail = models.BooleanField(default=False)
    jail_release_time = models.DateTimeField(null=True, blank=True)
    is_in_hospital = models.BooleanField(default=False)
    hospital_release_time = models.DateTimeField(null=True, blank=True)
    
    # Character type
    CHARACTER_CHOICES = [
        ('criminal', 'Criminal'),
        ('police', 'Police Officer'),
    ]
    character_type = models.CharField(max_length=10, choices=CHARACTER_CHOICES, default='criminal')
    
    # Money
    money = models.DecimalField(max_digits=15, decimal_places=2, default=1000.00)
    bank_money = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Location
    current_location = models.CharField(max_length=50, default='Home City')
    
    def __str__(self):
        return f"{self.user.username_display}'s Profile"