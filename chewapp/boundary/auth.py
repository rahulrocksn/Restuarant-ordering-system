from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout

from chewapp.boundary.templates import getSelectableProfiles


class LoginUI:
    def __init__(self, controller):
        self.controller = controller

    def DisplayPage(self, request):

        profiles = getSelectableProfiles()

        context = {"profiles": profiles}
        return render(request, "chewapp/login.html", context)

    def OnSubmit(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        userType = request.POST["userType"]

        # Setting username in session
        request.session["username"] = username

        ok, err = self.controller.Login(request, username, password, userType)
        if ok:
            userType = int(userType)
            # TODO: redirect to correct UserType dashboard
            # Check if the user has owner permissions:

            if userType == 1:
                return redirect("manager/menu")
            elif userType == 2:
                return redirect("admin/accounts/")
            elif userType == 3:  # Owner
                return redirect("owner/numberOfVisits/")
            elif userType == 4:
                return redirect("staff/orders/new")

        # Not OK, print error
        print(err)
        return HttpResponse("Error logging in: " + str(err))


class LogoutUI:
    def __init__(self):
        pass

    def DisplayPage(self, request):
        return self.Logout(request)

    def Logout(self, request):
        logout(request)
        return redirect("/login")
