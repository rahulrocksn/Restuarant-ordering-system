from django.contrib.auth.models import User
from django.db import transaction
from typing import List
from ..common.error import Result, Error
from ..models import Account, UserProfile


class CreateUsersController:
    def CreateAccount(
        self, username, password, profile_id, email=None
    ) -> Result[Account]:
        try:
            if email is None:
                email = f"{username}@localhost"
            # Perform operations in a transaction
            with transaction.atomic():
                # Get the profile
                profile = UserProfile.objects.get(id=profile_id)
                # Create a Django user
                user = User.objects.create_user(username, email, password)

                # Create the Account object
                account = Account(user=user, profile=profile)
                account.save()

                # Return the Account
                return account, None
        except Exception as ex:
            return None, Error(500, str(ex))


class AssignProfileController:
    def AssignProfile(self, username, profile_id) -> Result[Account]:
        try:
            # Get the profile
            profile = UserProfile.objects.get(id=profile_id)

            # Get the Account object
            account = Account.GetByUsername(username)

            # Assign the profile
            account.profile = profile
            account.save()
            return account, None
        except Exception as ex:
            return None, Error(500, str(ex))


class SearchUsersController:
    def SearchUsers(self, username) -> Result[List[Account]]:
        try:
            return Account.SearchUsers(username), None
        except Exception as ex:
            return None, Error(500, str(ex))


class ViewUserController:
    def ViewUser(self, username) -> Result[Account]:
        try:
            return Account.GetByUsername(username), None
        except Exception as ex:
            return None, Error(500, str(ex))


class SuspendUserController:
    def SuspendUser(self, username) -> Result[Account]:
        try:
            acc = Account.GetByUsername(username).Suspend()
            acc.save()
            return acc, None
        except Exception as ex:
            return None, Error(500, str(ex))


class UnsuspendUserController:
    def UnsuspendUser(self, username) -> Result[Account]:
        try:
            acc = Account.GetByUsername(username).Unsuspend()
            acc.save()
            return acc, None
        except Exception as ex:
            return None, Error(500, str(ex))


class ModifyUserController:
    def ModifyUser(
        self, id, *, username=None, password=None, email=None
    ) -> Result[Account]:
        try:
            acc = Account.GetByUserID(id)

            if username is not None:
                acc.user.username = username
            if password is not None:
                acc.user.set_password(password)
            if email is not None:
                acc.user.email = email

            acc.user.save()

            return acc, None
        except Exception as ex:
            return None, Error(500, str(ex))


class CreateUserProfileController:
    def CreateNewUserProfile(
        self,
        name,
        *,
        manager=False,
        administrator=False,
        owner=False,
        staff=False,
    ) -> Result[UserProfile]:
        try:
            profile = UserProfile(
                name=name,
                is_manager=manager,
                is_administrator=administrator,
                is_owner=owner,
                is_staff=staff,
            )
            profile.save()
            return profile, None
        except Exception as ex:
            return None, Error(500, str(ex))


class ModifyUserProfileController:
    def ModifyUserProfile(
        self,
        id,
        *,
        name=None,
        manager=None,
        administrator=None,
        owner=None,
        staff=None,
    ) -> Result[UserProfile]:
        try:
            # Fetch the profile
            profile = UserProfile.GetByID(id)

            # Update
            if name is not None:
                profile.name = name
            if manager is not None:
                profile.is_manager = manager
            if administrator is not None:
                profile.is_administrator = administrator
            if owner is not None:
                profile.is_owner = owner
            if staff is not None:
                profile.is_staff = staff
            profile.save()

            return profile, None
        except Exception as ex:
            return None, Error(500, str(ex))


class DeleteUserProfileController:
    def DeleteUserProfile(self, id) -> Result[UserProfile]:
        try:
            # Fetch the profile
            profile = UserProfile.GetByID(id)

            # Delete it
            profile.delete()

            return profile, None
        except Exception as ex:
            return None, Error(500, str(ex))


class ViewUserProfileController:
    def ViewUserProfile(self, id) -> Result[UserProfile]:
        try:
            return UserProfile.GetByID(id), None
        except Exception as ex:
            return None, Error(500, str(ex))


class ListUserProfilesController:
    def ListUserProfiles(self) -> Result[List[UserProfile]]:
        try:
            return UserProfile.GetAll(), None
        except Exception as ex:
            return None, Error(500, str(ex))


class SearchUserProfilesController:
    def SearchUserProfiles(self, keyword) -> Result[List[UserProfile]]:
        try:
            return UserProfile.SearchUserProfiles(keyword), None
        except Exception as ex:
            return None, Error(500, str(ex))
