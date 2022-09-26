from django.shortcuts import render, HttpResponse
from ..common.auth_decorator import with_auth


class SampleBoundary:
    def __init__(self, controller):
        self.controller = controller

    def index(self, request):
        return render(request, "menu/index.html")

    def systime(self, request):
        time, err = self.controller.get_systime()
        if err is None:
            return HttpResponse("The time is: %s" % time)
        return HttpResponse(err)

    # Example of a view that has context passed into a template.
    @with_auth(administrator=True)
    def adminSample(self, request):
        context = {
            "username": "admin101",
            "profile": "admin",
            "abc": "this will be passed into the template by calling {{abc}}",
            "tabs": ["Menu Items", "Coupons", "Categories"],
            "activeTab": "Menu Items",
            "searchBar": True,
            "createButton": True,
        }
        return render(request, "chewapp/admin.html", context)
