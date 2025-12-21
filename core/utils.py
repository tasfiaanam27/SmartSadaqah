from .models import UserProfile


def is_donor(user):
    if not user or not user.is_authenticated:
        return False
    try:
        return user.profile.role == UserProfile.ROLE_DONOR
    except UserProfile.DoesNotExist:
        return False


def is_recipient(user):
    if not user or not user.is_authenticated:
        return False
    try:
        return user.profile.role == UserProfile.ROLE_RECIPIENT
    except UserProfile.DoesNotExist:
        return False


def is_admin(user):
    if not user or not user.is_authenticated:
        return False
    try:
        return user.profile.role == UserProfile.ROLE_ADMIN
    except UserProfile.DoesNotExist:
        return False

