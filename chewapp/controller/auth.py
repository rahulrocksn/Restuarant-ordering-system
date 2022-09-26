from django.contrib.auth import authenticate, login, logout
from typing import List
from ..common.error import Result, Error
from ..models import Account, UserProfile


class LoginController:
    def ListUserProfiles(self) -> Result[List[UserProfile]]:
        try:
            return UserProfile.GetAll(), None
        except Exception as ex:
            return None, Error(500, str(ex))

    def Login(self, request, username, password, userProfileID) -> Result[bool]:
        # Authenticate using Django
        user = authenticate(request, username=username, password=password)

        if user is None:
            # Auth failed, return error
            return False, Error(401, "Invalid login")

        # Check if we have the Account
        try:
            account = Account.GetByUsername(user)
        except Account.DoesNotExist as ex:
            # Account improperly created
            return False, Error(401, "Invalid login")

        # Make sure account is not suspended
        if account.is_suspended:
            return False, Error(403, "Account is suspended")

        # Check if the user profile has the permissions required
        userProfileID = int(userProfileID)

        if userProfileID == 1 and not account.profile.is_manager:
            return False, Error(403, "Not a manager")
        elif userProfileID == 2 and not account.profile.is_administrator:
            return False, Error(403, "Not an admin")
        elif userProfileID == 3 and not account.profile.is_owner:
            return False, Error(403, "Not an owner")
        elif userProfileID == 4 and not account.profile.is_staff:
            return False, Error(403, "Not a staff")

        # Log the user in
        login(request, user)

        # Return
        return True, None
