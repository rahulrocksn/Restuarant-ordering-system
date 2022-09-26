from django.contrib.auth.models import User
from chewapp.models import Account, UserProfile

user = User.objects.get(id=1)
profile = UserProfile.objects.get(id=5)
Account(user=user, profile=profile).save()
