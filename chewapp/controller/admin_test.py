from django.test import TestCase
from .admin import (
    CreateUsersController,
    SearchUsersController,
    ViewUserController,
    SuspendUserController,
    UnsuspendUserController,
    ModifyUserController,
    AssignProfileController,
    CreateUserProfileController,
    ModifyUserProfileController,
    ViewUserProfileController,
    ListUserProfilesController,
    DeleteUserProfileController,
)
from ..common.error import Result, Error


class TestAdminController(TestCase):
    def setUp(self):
        pass

    def test_users_controller(self):
        # Create a new user
        c = CreateUsersController()
        account, err = c.CreateAccount("admin", "password123", 1)
        self.assertEqual(err, None)
        self.assertEqual(account.user.username, "admin")
        self.assertEqual(account.profile.id, 1)
        userid = account.user.id

        # Search the newly created user
        c = SearchUsersController()
        accounts, err = c.SearchUsers("dMi")
        self.assertEqual(err, None)
        self.assertEqual(len(accounts), 1)

        # Search nonexistent user
        accounts, err = c.SearchUsers("asdf")
        self.assertEqual(err, None)
        self.assertEqual(len(accounts), 0)

        # Get the user by username
        c = ViewUserController()
        acc, err = c.ViewUser("admin")
        self.assertEqual(err, None)
        self.assertEqual(acc, account)

        # Get nonexistent user
        _, err = c.ViewUser("nobody")
        self.assertNotEqual(err, None)
        self.assertIsInstance(err, Error)

        # Suspend the user
        c = SuspendUserController()
        sus, err = c.SuspendUser("admin")
        self.assertEqual(err, None)
        self.assertTrue(sus.is_suspended)

        # Unsuspend the user
        c = UnsuspendUserController()
        sus, err = c.UnsuspendUser("admin")
        self.assertEqual(err, None)
        self.assertFalse(sus.is_suspended)

        # Assign a profile to the user
        c = AssignProfileController()
        account, err = c.AssignProfile("admin", 3)
        self.assertEqual(err, None)
        self.assertEqual(account.profile.id, 3)

        # Change the user's details
        c = ModifyUserController()
        account, err = c.ModifyUser(userid, username="mike", password="asdf")
        self.assertEqual(err, None)
        self.assertEqual(account.user.username, "mike")

    def test_user_profile(self):
        # Create a new user profile
        c = CreateUserProfileController()
        profile, err = c.CreateNewUserProfile("test profile", manager=True, owner=True)
        self.assertEqual(err, None)
        self.assertTrue(profile.is_manager)
        self.assertFalse(profile.is_administrator)
        self.assertEqual(profile.name, "test profile")

        # Get the user profile
        c = ViewUserProfileController()
        p, err = c.ViewUserProfile(profile.id)
        self.assertEqual(err, None)
        self.assertEqual(p, profile)

        # List all the profiles
        c = ListUserProfilesController()
        ps, err = c.ListUserProfiles()
        self.assertEqual(err, None)
        self.assertTrue(profile in ps)
        self.assertTrue(len(ps) > 0)

        # Change some things
        c = ModifyUserProfileController()
        new, err = c.ModifyUserProfile(
            profile.id, name="modified profile", manager=False, administrator=True
        )
        self.assertEqual(err, None)
        self.assertEqual(new.name, "modified profile")
        self.assertFalse(new.is_manager)
        self.assertTrue(new.is_administrator)
        self.assertTrue(new.is_owner)
        self.assertFalse(new.is_staff)

        # Try to modify nonexistent profile
        _, err = c.ModifyUserProfile(999, name="test")
        self.assertNotEqual(err, None)
        self.assertIsInstance(err, Error)

        # Delete the profile
        c = DeleteUserProfileController()
        _, err = c.DeleteUserProfile(profile.id)
        self.assertEqual(err, None)

        # Make sure profile is deleted
        c = ViewUserProfileController()
        p, err = c.ViewUserProfile(profile.id)
        self.assertEqual(p, None)
        self.assertNotEqual(err, None)
        self.assertIsInstance(err, Error)
