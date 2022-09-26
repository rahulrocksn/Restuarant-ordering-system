from cmath import exp
from multiprocessing import context
from select import select
from django.shortcuts import redirect, render, HttpResponse
from django.http import QueryDict
from chewapp.common.auth_decorator import with_auth

from chewapp.common.error import Error
from chewapp.controller.admin import (
    AssignProfileController,
    CreateUserProfileController,
    DeleteUserProfileController,
    ListUserProfilesController,
    ModifyUserController,
    ModifyUserProfileController,
    SearchUserProfilesController,
    SearchUsersController,
    SuspendUserController,
    UnsuspendUserController,
    ViewUserController,
    ViewUserProfileController,
)
from .templates import getTabs, getTabsAdmin
from django.utils.datastructures import MultiValueDictKeyError


class SearchUsersUI:
    def __init__(self, controller: SearchUsersController) -> None:
        self.controller = controller

    @with_auth(administrator=True)
    def DisplayPage(self, request) -> render:

        # Check if there is any data in the request for search

        SearchTerm = request.GET.get("searchTerm", "")

        # Get the menu items from the controller.

        users, error = self.controller.SearchUsers(SearchTerm)

        if not error:

            UserAccounts = list()

            for user in users:
                UserAccount = dict()
                UserAccount["id"] = user.id
                UserAccount["is_suspended"] = user.is_suspended
                UserAccount["username"] = user.user.username
                UserAccount["email"] = user.user.email
                UserAccounts.append(UserAccount)

            context = {
                "username": request.session.get("username", "error"),
                "profile": "admin",
                "tabs": getTabsAdmin(request, "Users"),
                "activeTab": "Users",
                "searchBar": True,
                "createButton": request.build_absolute_uri("/admin/accounts/create"),
                "UserAccounts": UserAccounts,
                "searchBarHome": request.build_absolute_uri("/admin/accounts"),
                "searchBarLink": request.build_absolute_uri("/admin/accounts"),
            }

            if SearchTerm != "":
                context["searchBar"] = SearchTerm

            return self.DisplayAccounts(request, context)

        else:
            self.DisplayError(error)

    @with_auth(administrator=True)
    def DisplayAccounts(self, request, context) -> render:
        return render(
            request,
            "chewapp/AdminViewUserAccounts.html",
            context,
        )

    @with_auth(administrator=True)
    def DisplayError(error: Error) -> HttpResponse:
        return HttpResponse(str(error))


class SearchUserProfilesUI:
    def __init__(self, controller: SearchUserProfilesController) -> None:
        self.controller = controller

    @with_auth(administrator=True)
    def DisplayPage(self, request) -> render:

        # Check if there is any data in the request for search

        SearchTerm = request.GET.get("searchTerm", "")

        profiles, error = self.controller.SearchUserProfiles(SearchTerm)

        if not error:

            UserProfiles = list()

            for profile in profiles:
                UserProfile = dict()
                UserProfile["id"] = profile.id
                UserProfile["name"] = profile.name

                UserProfiles.append(UserProfile)

            context = {
                "username": request.session.get("username", "error"),
                "profile": "admin",
                "tabs": getTabsAdmin(request, "User Profiles"),
                "activeTab": "User Profiles",
                "searchBar": True,
                "createButton": request.build_absolute_uri("/admin/profiles/create"),
                "UserProfiles": UserProfiles,
                "searchBarHome": request.build_absolute_uri("/admin/profiles"),
                "searchBarLink": request.build_absolute_uri("/admin/profiles"),
            }

            if SearchTerm != "":
                context["searchBar"] = SearchTerm

            return self.DisplayUserProfiles(request, context)

        else:
            self.DisplayError(error)

    @with_auth(administrator=True)
    def DisplayUserProfiles(self, request, context) -> render:
        return render(
            request,
            "chewapp/AdminViewUserProfiles.html",
            context,
        )

    @with_auth(administrator=True)
    def DisplayError(error: Error) -> HttpResponse:
        return HttpResponse(str(error))


class CreateUserProfileUI:
    def __init__(self, controller: CreateUserProfileController) -> None:
        self.controller = controller

    @with_auth(administrator=True)
    def DisplayPage(self, request):

        context = {"TitleText": "Create User Profile"}

        return render(
            request,
            "chewapp/AdminCreateUserProfile.html",
            context,
        )

    @with_auth(administrator=True)
    def OnSubmit(self, request) -> HttpResponse:

        # Get the form data from the request.

        try:
            formData = request.POST
            RoleName = formData.get("RoleName")
            Staff = formData.get("Staff", False) == "on"
            Admin = formData.get("Admin", False) == "on"
            Manager = formData.get("Manager", False) == "on"
            Owner = formData.get("Owner", False) == "on"

        except MultiValueDictKeyError:
            self.DisplayError(request, Error("Invalid form data"))
            pass

        # Create the user profile.

        userProfile, error = self.controller.CreateNewUserProfile(
            name=RoleName,
            manager=Manager,
            administrator=Admin,
            owner=Owner,
            staff=Staff,
        )

        if not error:

            return self.DisplaySuccess(request)

        else:
            self.DisplayError(request, error)

    @with_auth(administrator=True)
    def DisplayError(self, request, error: Error) -> HttpResponse:

        context = {"TitleText": "Create User Profile", "Error": str(error)}

        return render(
            request,
            "chewapp/AdminCreateUserProfile.html",
            context,
        )

    @with_auth(administrator=True)
    def DisplaySuccess(self, request) -> redirect:

        return redirect("/admin/profiles")


class CreateUserAccountUI:
    def __init__(self, ListUserProfileController, CreateUsersController) -> None:
        self.ListUserProfilesController = ListUserProfileController
        self.CreateUsersController = CreateUsersController

    @with_auth(administrator=True)
    def DisplayPage(self, request) -> render:

        # Get the list of user profiles.
        Profiles, error = self.ListUserProfilesController.ListUserProfiles()

        if not error:

            context = {"TitleText": "Create User Account", "Profiles": Profiles}

            return render(
                request,
                "chewapp/AdminCreateUserAccount.html",
                context,
            )

        else:
            self.DisplayError(request, error)

    @with_auth(administrator=True)
    def OnSubmit(self, request) -> HttpResponse:

        # Get the data from the request.

        Username = request.POST.get("Username", "")
        Email = request.POST.get("Email", "")
        Password = request.POST.get("Password", "")
        ConfirmPassword = request.POST.get("ConfirmPassword", "")
        Profile = request.POST.get("Profile", "")

        # Check if the data is valid.

        if (
            Username == ""
            or Email == ""
            or Password == ""
            or ConfirmPassword == ""
            or Profile == ""
        ):
            error = Error(
                "500",
                "Please fill in all fields.",
            )
            return self.DisplayError(request, error)

        if Password != ConfirmPassword:
            error = Error(
                "Passwords do not match.",
                "Please ensure that the passwords match.",
            )
            return self.DisplayError(request, error)

        # Create the user account.

        account, error = self.CreateUsersController.CreateAccount(
            username=Username, password=Password, email=Email, profile_id=Profile
        )

        if not error:
            return self.RedirectToDashboard(request)

        else:
            return self.DisplayError(request, error)

    @with_auth(administrator=True)
    def DisplayError(self, request, error: Error) -> render:

        Profiles, error2 = self.ListUserProfilesController.ListUserProfiles()

        if not error2:

            context = {
                "TitleText": "Create User Account",
                "Profiles": Profiles,
                "Error": str(error),
            }

            return render(
                request,
                "chewapp/AdminCreateUserAccount.html",
                context,
            )

        else:

            context = {
                "TitleText": "Create User Account",
                "Profiles": Profiles,
                "Error": "\n".join([str(error), str(error2)]),
            }

            return render(
                request,
                "chewapp/AdminCreateUserAccount.html",
                context,
            )

    @with_auth(administrator=True)
    def RedirectToDashboard(self, request) -> redirect:
        return redirect("/admin/accounts")


class ModifyUserProfileUI:
    def __init__(
        self,
        ViewUserProfileController: ViewUserProfileController,
        ModifyUserProfileController: ModifyUserProfileController,
    ) -> None:
        self.ViewUserProfileController = ViewUserProfileController
        self.ModifyUserProfileController = ModifyUserProfileController

    @with_auth(administrator=True)
    def DisplayPage(self, request, id) -> render:

        profile, error = self.ViewUserProfileController.ViewUserProfile(id)

        if not error:

            context = {
                "TitleText": "Modify User Profile",
                "RoleName": profile.name,
                "Staff": profile.is_staff,
                "Admin": profile.is_administrator,
                "Manager": profile.is_manager,
                "Owner": profile.is_owner,
            }

            return render(
                request,
                "chewapp/AdminModifyUserProfile.html",
                context,
            )

        else:
            self.DisplayError(request, error)

    @with_auth(administrator=True)
    def OnSubmit(self, request, id) -> HttpResponse:

        # Get the form data from the request.

        try:
            formData = request.POST
            RoleName = formData.get("RoleName")
            Staff = formData.get("Staff", False) == "on"
            Admin = formData.get("Admin", False) == "on"
            Manager = formData.get("Manager", False) == "on"
            Owner = formData.get("Owner", False) == "on"

        except MultiValueDictKeyError:
            self.DisplayError(request, Error(422, "Invalid form data"))

        # Modify the user profile.

        profile, error = self.ModifyUserProfileController.ModifyUserProfile(
            id,
            name=RoleName,
            manager=Manager,
            administrator=Admin,
            owner=Owner,
            staff=Staff,
        )

        if not error:

            return self.DisplayUserProfiles(request)

        else:
            self.DisplayError(request, error)

    @with_auth(administrator=True)
    def DisplayError(self, request, error: Error) -> HttpResponse:

        context = {"TitleText": "Modify User Profile", "Error": str(error)}

        return render(
            request,
            "chewapp/AdminModifyUserProfile.html",
            context,
        )

    @with_auth(administrator=True)
    def DisplayUserProfiles(self, request) -> redirect:
        return redirect("/admin/profiles")


class ModifyUserAccountUI:
    def __init__(
        self,
        ListUserProfileController: ListUserProfilesController,
        ModifyUserController: ModifyUserController,
        AssignProfileController: AssignProfileController,
        ViewUserController: ViewUserController,
    ) -> None:
        self.ListUserProfilesController = ListUserProfileController
        self.ModifyUserController = ModifyUserController
        self.AssignProfileController = AssignProfileController
        self.ViewUserController = ViewUserController

    @with_auth(administrator=True)
    def DisplayPage(self, request, username) -> render:

        # Get the list of user profiles.
        Profiles, error = self.ListUserProfilesController.ListUserProfiles()

        User, error2 = self.ViewUserController.ViewUser(username)

        if not error:

            context = {
                "TitleText": "Modify User Account",
                "ID": User.id,
                "Profiles": Profiles,
                "Username": User.user.username,
                "Email": User.user.email,
                "CurrentProfile": User.profile.id,
            }

            return render(
                request,
                "chewapp/AdminModifyUserAccount.html",
                context,
            )

        else:
            self.DisplayError(request, error)

    @with_auth(administrator=True)
    def OnSubmit(self, request, username) -> HttpResponse:

        # Get the data from the request.

        ID = request.POST.get(
            "ID", ""
        )  # Because the sequence is a ID. Grab it from hidden field.
        Username = request.POST.get("Username", "")
        Email = request.POST.get("Email", "")
        Password = request.POST.get("Password", "")
        ConfirmPassword = request.POST.get("ConfirmPassword", "")
        Profile = request.POST.get("Profile", "")

        # Check if the data is valid.
        if Username == "" or Email == "" or Profile == "" or ID == "":
            error = Error(
                500,
                "Please fill in all fields.",
            )
            return self.DisplayError(request, error, username)

        passwordChange = False
        # Checking if the password has changed.
        if Password != "":
            if Password != ConfirmPassword:
                error = Error(
                    "Passwords do not match.",
                    "Please ensure that the passwords match.",
                )
                return self.DisplayError(request, error, username)
            else:
                passwordChange = True

        # Modify the user account.

        if passwordChange:
            user, error = self.ModifyUserController.ModifyUser(
                id=ID,
                username=Username,
                email=Email,
                password=Password,
            )
        else:
            user, error = self.ModifyUserController.ModifyUser(
                id=ID,
                username=Username,
                email=Email,
            )

        if error:
            return self.DisplayError(request, error, username)

        # Profile change

        _, error2 = self.AssignProfileController.AssignProfile(Username, Profile)

        if error2:
            return self.DisplayError(request, error2, username)

        return redirect("/admin/accounts")

    @with_auth(administrator=True)
    def DisplayError(self, request, error: Error, username) -> render:

        Profiles, error2 = self.ListUserProfilesController.ListUserProfiles()

        User, error3 = self.ViewUserController.ViewUser(username)

        if not error2:

            context = {
                "TitleText": "Modify User Account",
                "ID": User.id,
                "Profiles": Profiles,
                "Username": User.user.username,
                "Email": User.user.email,
                "CurrentProfile": User.profile.id,
                "Error": "\n".join([str(error), str(error2)]),
            }

            return render(
                request,
                "chewapp/AdminModifyUserAccount.html",
                context,
            )

        else:

            context = {
                "TitleText": "Modify User Account",
                "ID": User.id,
                "Username": User.user.username,
                "Email": User.user.email,
                "CurrentProfile": User.profile.id,
                "Error": "Critical Error. Please try Refresh.",
            }

            return render(
                request,
                "chewapp/AdminModifyUserAccount.html",
                context,
            )


class SuspendUserAccountUI:
    def __init__(self, SuspendUserController: SuspendUserController) -> None:
        self.SuspendUserController = SuspendUserController

    @with_auth(administrator=True)
    def OnSubmit(self, request, username) -> HttpResponse:

        # Suspend the user account.

        _, error = self.SuspendUserController.SuspendUser(username)

        if not error:

            return self.RedirectToDashboard(request)

        else:
            return self.DisplayError(request, error)

    @with_auth(administrator=True)
    def RedirectToDashboard(self, request) -> HttpResponse:

        return HttpResponse("ok")

    @with_auth(administrator=True)
    def DisplayError(self, request, error: Error) -> HttpResponse:

        return HttpResponse(f"Error {error}", status=500)


class UnsuspendUserAccountUI:
    def __init__(self, UnsuspendUserController: UnsuspendUserController) -> None:
        self.UnsuspendUserController = UnsuspendUserController

    @with_auth(administrator=True)
    def OnSubmit(self, request, username) -> HttpResponse:

        # Suspend the user account.

        _, error = self.UnsuspendUserController.UnsuspendUser(username)

        if not error:

            return self.RedirectToDashboard(request)

        else:
            return self.RedirectToDashboard(request)

    @with_auth(administrator=True)
    def RedirectToDashboard(self, request) -> HttpResponse:

        return HttpResponse("ok")

    @with_auth(administrator=True)
    def DisplayError(self, request, error) -> HttpResponse:

        return HttpResponse(f"Error {error}", status=500)


class DeleteUserProfileUI:
    def __init__(
        self, DeleteUserProfileController: DeleteUserProfileController
    ) -> None:
        self.DeleteUserProfileController = DeleteUserProfileController

    @with_auth(administrator=True)
    def OnSubmit(self, request, id) -> HttpResponse:

        # Delete the user profile.

        _, error = self.DeleteUserProfileController.DeleteUserProfile(id)

        if not error:

            return self.RedirectToDashboard(request)

        else:
            return self.DisplayError(request, error)

    @with_auth(administrator=True)
    def RedirectToDashboard(self, request) -> HttpResponse:

        return HttpResponse("ok")

    @with_auth(administrator=True)
    def DisplayError(self, request, error: Error) -> HttpResponse:

        return HttpResponse(f"Error {error}", status=500)
