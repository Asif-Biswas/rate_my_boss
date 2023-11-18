from .models import UserProfile

def user_profile(request):
    """
    This is a context processor for user profile.
    """
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        return {'user_profile': user_profile}
    return {}