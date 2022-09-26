import json
from django.shortcuts import redirect, render, HttpResponse
from chewapp.common.auth_decorator import with_auth
from chewapp.common.error import Error

from chewapp.controller.manager import (
    AddCategoryController,
    CreateCouponCodeController,
    CreateNewMenuItemController,
    DeleteCouponCodeController,
    DeleteMenuItemController,
    GetAllCouponCodeController,
    ModifyMenuItemController,
    SearchMenuItemController,
    ViewCategoryController,
    ViewCouponCodeController,
    ViewMenuController,
    DeleteCategoryController,
    SearchCouponCodeController,
    SearchCategoryController,
    ModifyCategoryController,
)
from chewapp.models import MenuItem
from .templates import getTabs
from django.utils.datastructures import MultiValueDictKeyError
from django.http import QueryDict


class ViewMenuUI:
    def __init__(self, controller: ViewMenuController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):

        try:
            rawMenuItems, error = self.controller.GetMenuItems()

            if not error:

                menuItems = [
                    {
                        "MenuItemID": item.id,
                        "Name": item.name,
                        "Price": item.price,
                        "Description": item.description,
                        "img": item.menuImg.url,
                    }
                    for item in rawMenuItems
                ]

                context = {
                    "username": request.session.get("username", "error"),
                    "profile": "manager",
                    "tabs": getTabs(request, "Menu Items"),
                    "activeTab": "Menu Items",
                    "searchBar": True,
                    "createButton": request.build_absolute_uri("/manager/menu/create"),
                    "menuItems": menuItems,
                    "searchBarLink": request.build_absolute_uri("/manager/menu/search"),
                }
                return render(request, "chewapp/ManagerMenuItems.html", context)
            else:
                return self.DisplayError(request, error)

        except Exception as ex:
            return self.DisplayError(request, str(ex))

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/menu"),
            },
        )


class DeleteMenuItemUI:
    def __init__(self, controller: DeleteMenuItemController):
        self.controller = controller

    @with_auth(manager=True)
    def OnSubmit(self, request, MenuItemID):

        try:
            _, error = self.controller.DeleteMI(MenuItemID)

            if not error:
                return HttpResponse("ok")
            else:
                return HttpResponse(str(error), status=500)
        except Exception as ex:
            return HttpResponse(str(ex), status=500)


class SearchMenuItemUI:
    def __init__(self, controller: SearchMenuItemController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):

        try:

            searchTerm = request.GET["searchTerm"]

            if searchTerm == "":
                raise Exception("Search term cannot be empty")

            rawMenuItems, error = self.controller.SearchMI(searchTerm)

            if not error:
                menuItems = [
                    {
                        "MenuItemID": item.id,
                        "Name": item.name,
                        "Price": item.price,
                        "Description": item.description,
                        "img": item.menuImg.url,
                    }
                    for item in rawMenuItems
                ]

                context = {
                    "username": request.session.get("username", "error"),
                    "profile": "manager",
                    "tabs": getTabs(request, "Menu Items"),
                    "searchBar": searchTerm,
                    "createButton": request.build_absolute_uri("/manager/menu/create"),
                    "activeTab": "Menu Items",
                    "menuItems": menuItems,
                    "searchBarHome": request.build_absolute_uri("/manager/menu/search"),
                    "searchBarLink": request.build_absolute_uri("/manager/menu/search"),
                }

                return render(request, "chewapp/ManagerSearchMenuItems.html", context)

            else:
                return HttpResponse(str(error), status=500)

        except Exception:
            return redirect("/manager/menu")


class ModifyMenuItemUI:
    def __init__(
        self,
        deleteMenuItemController: DeleteMenuItemController,
        viewMenuController: ViewMenuController,
        modifyMenuItemController: ModifyMenuItemController,
    ):
        self.deleteMenuItemController = deleteMenuItemController
        self.viewMenuController = viewMenuController
        self.modifyMenuItemController = modifyMenuItemController

    @with_auth(manager=True)
    def DisplayPage(self, request, MenuItemID):

        # Get the menu item from the controller.
        try:
            menuItem, error = self.viewMenuController.ViewMI(MenuItemID)

            if error is not None:
                return self.DisplayError(request, error)

            context = {
                "TitleText": "Modify Menu Item",
                "Name": menuItem.name,
                "Price": menuItem.price,
                "Description": menuItem.description,
                "OutOfStock": menuItem.stock,
                "itemId": menuItem.id,
                "img": menuItem.menuImg.url,
            }

            return render(request, "chewapp/ManagerModifyMenuItem.html", context)

        except Exception as ex:
            return self.DisplayError(request, str(ex))

    @with_auth(manager=True)
    def OnSubmit(self, request, MenuItemID):

        try:

            File = request.FILES.get("Picture", None)

            Name = request.POST.get("Name")
            Price = request.POST.get("Price")
            Description = request.POST.get("Description", "")
            StockStatus = request.POST.get("StockStatus", False)

            StockStatus = True if StockStatus == "true" else False

            _, error = self.modifyMenuItemController.ModifyMI(
                MIID=MenuItemID,
                Name=Name,
                Price=Price,
                Desc=Description,
                Stock=StockStatus,
                File=File,
            )

            if not error:
                return HttpResponse("ok")
            else:
                print(error)
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            return HttpResponse(str(ex), status=500)

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/menu"),
            },
        )


class CreateMenuItemUI:
    def __init__(self, controller: CreateNewMenuItemController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):

        context = {"TitleText": "Create Menu Item"}

        return render(request, "chewapp/ManagerCreateMenuItem.html", context)

    @with_auth(manager=True)
    def OnSubmit(self, request):

        try:

            Photo = request.FILES.get("Picture")

            # Get the data from the form.
            Name = request.POST.get("Name")
            Price = request.POST.get("Price")
            Description = request.POST.get("Description", "")
            StockStatus = request.POST.get("StockStatus", False)

            # Call the controller to create the menu item.
            _, error = self.controller.CreateNewMI(
                Name=Name, Price=Price, Desc=Description, Stock=StockStatus, File=Photo
            )

            if not error:
                return redirect("/manager/menu")
            else:
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            return HttpResponse(str(ex), status=500)


# Categories
class ViewCategoryUI:
    def __init__(self, controller: ViewCategoryController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):

        try:
            rawCC, error = self.controller.ViewCategory()

            if not error:

                categories = [
                    {
                        "CID": item.id,
                        "Name": item.name,
                    }
                    for item in rawCC
                ]

                context = {
                    "username": request.session.get("username", "error"),
                    "profile": "manager",
                    "tabs": getTabs(request, "Categories"),
                    "activeTab": "Categories",
                    "searchBar": True,
                    "createButton": True,
                    "categories": categories,
                    "createButton": request.build_absolute_uri("/manager/category/add"),
                    "searchBarLink": request.build_absolute_uri(
                        "/manager/category/search"
                    ),
                }
                return render(request, "chewapp/ManagerCategories.html", context)

            else:
                return self.DisplayError(request, error)

        except Exception as ex:
            return self.DisplayError(request, str(ex))

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/category"),
            },
        )


class DeleteCategoryUI:
    def __init__(self, controller: DeleteCategoryController):
        self.controller = controller

    @with_auth(manager=True)
    def OnSubmit(self, request, CID):

        try:
            _, error = self.controller.DeleteCategory(CID)

            if not error:
                return HttpResponse("Ok")
            else:
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            self.DisplayError(request, Error(500, str(ex)))

    @with_auth(manager=True)
    def DisplayError(self, request, error: Error):
        return HttpResponse(str(error), status=error.code)


class SearchCategoryUI:
    def __init__(self, controller: SearchCategoryController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):

        try:

            searchTerm = request.GET["searchTerm"]

            if searchTerm == "":
                raise Exception("Search term cannot be empty")

            rawC, error = self.controller.SearchCategory(searchTerm)

            if not error:
                categories = [
                    {
                        "CID": item.id,
                        "Name": item.name,
                    }
                    for item in rawC
                ]

                context = {
                    "username": request.session.get("username", "error"),
                    "profile": "manager",
                    "tabs": getTabs(request, "Categories"),
                    "searchBar": searchTerm,
                    "createButton": request.build_absolute_uri("/manager/category/add"),
                    "activeTab": "Categories",
                    "categories": categories,
                    "searchBarHome": request.build_absolute_uri(
                        "/manager/category/search"
                    ),
                    "searchBarLink": request.build_absolute_uri(
                        "/manager/category/search"
                    ),
                }

                return render(request, "chewapp/ManagerSearchCategories.html", context)

            else:
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            return self.DisplayError(request, Error(500, str(ex)))

    @with_auth(manager=True)
    def DisplayError(self, request, error: Error):
        print(error)
        return redirect("/manager/category")


class AddCategoryUI:
    def __init__(
        self,
        addCategoryController: AddCategoryController,
        viewMenuController: ViewMenuController,
    ):
        self.addCategoryController = addCategoryController
        self.viewMenuController = viewMenuController

    @with_auth(manager=True)
    def DisplayPage(self, request):

        try:

            RAWMenuItems, MenuItemError = self.viewMenuController.GetMenuItems()

            if MenuItemError is not None:
                return self.DisplayError(request, MenuItemError)

            menuItems = [{"ID": item.id, "Name": item.name} for item in RAWMenuItems]

            context = {
                "username": request.session.get("username", "error"),
                "profile": "manager",
                "tabs": getTabs(request, "Categories"),
                "activeTab": "Categories",
                "searchBar": True,
                "createButton": True,
                "MenuItems": menuItems,
                "createButton": request.build_absolute_uri("/manager/category/add"),
                "searchBarLink": request.build_absolute_uri("/manager/category/search"),
            }
            return render(request, "chewapp/ManagerAddCategories.html", context)

        except Exception as ex:
            return self.DisplayError(request, str(ex))

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/category"),
            },
        )

    @with_auth(manager=True)
    def OnSubmit(self, request):

        try:
            data = QueryDict(request.body)
            Name = data.get("categoryName")
            desc = data.get("description", "")

            RAWMenuItems, MenuItemError = self.viewMenuController.GetMenuItems()

            if MenuItemError is not None:
                return self.DisplayError(request, MenuItemError)

            menuItems = [{"ID": item.id, "Checked": False} for item in RAWMenuItems]

            for i, item in enumerate(menuItems):
                checked = data.get(f"mi_{item['ID']}", False)

                if checked:
                    checked = True

                menuItems[i]["Checked"] = checked

            MIIDs = [item.get("ID") for item in menuItems if item["Checked"]]

            # Call the controller to create the menu item.
            _, error = self.addCategoryController.AddCategory(
                CatName=Name,
                Desc=desc,
                MIIDs=MIIDs,
            )

            if not error:
                return redirect("/manager/category")
            else:
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            return HttpResponse(str(ex), status=500)


class ModifyCategoryUI:
    def __init__(
        self,
        deleteCategoryController: DeleteCategoryController,
        viewCategoryController: ViewCategoryController,
        modifyCategoryController: ModifyCategoryController,
        viewMenuController: ViewMenuController,
    ):
        self.deleteCategoryController = deleteCategoryController
        self.viewCategoryController = viewCategoryController
        self.modifyCategoryController = modifyCategoryController
        self.viewMenuController = viewMenuController

    @with_auth(manager=True)
    def DisplayPage(self, request, CID):

        try:
            Category, CategoryError = self.viewCategoryController.GetCategory(CID)

            (
                CategoryMenu,
                CategoryMenuError,
            ) = self.viewCategoryController.GetCategoryMenuItems(CID)

            if CategoryError is not None:
                return self.DisplayError(request, CategoryError)

            (
                RAWMenuItems,
                MenuItemError,
            ) = self.viewMenuController.GetMenuItems()

            if MenuItemError is not None:
                return self.DisplayError(request, MenuItemError)

            CheckedMenuItems = [
                {"ID": item.id, "Name": item.name, "Selected": False}
                for item in RAWMenuItems
            ]

            for item in CheckedMenuItems:
                for menuItem in CategoryMenu:
                    if item["ID"] == menuItem.id:
                        item["Selected"] = True

            context = {
                "TitleText": "Modify Category Item",
                "CID": CID,
                "Name": Category.name,
                "desc": Category.description,
                "MenuItems": CheckedMenuItems,
            }

            return render(request, "chewapp/ManagerModifyCategories.html", context)

        except Exception as ex:
            return self.DisplayError(request, str(ex))

    @with_auth(manager=True)
    def OnSubmit(self, request, CID):

        try:

            data = json.loads(request.body)

            print(data)

            Name = data.get("Name")
            desc = data.get("description", "")
            MIIDs = data.get("MenuItems")

            print(MIIDs)

            _, error = self.modifyCategoryController.ModifyCategory(
                CID=CID,
                Name=Name,
                Desc=desc,
                MIIDs=MIIDs,
            )

            if not error:
                return HttpResponse("ok")
            else:
                print(error)
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            return HttpResponse(str(ex), status=500)

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/categories"),
            },
        )


# Coupon Codes


class ViewCouponCodeUI:
    def __init__(self, controller: GetAllCouponCodeController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):

        try:
            rawCC, error = self.controller.GetAllCouponCodes()

            if not error:

                couponCodes = [
                    {
                        "CID": item.id,
                        "Coupon": item.code,
                        "Percent": item.discount_percent,
                        "Dollar": item.discount_dollar,
                        "MinAmt": item.min_spend,
                    }
                    for item in rawCC
                ]

                context = {
                    "username": request.session.get("username", "error"),
                    "profile": "manager",
                    "tabs": getTabs(request, "Coupons"),
                    "activeTab": "Coupons",
                    "searchBar": True,
                    "createButton": True,
                    "couponCodes": couponCodes,
                    "createButton": request.build_absolute_uri(
                        "/manager/couponCodes/add"
                    ),
                    "searchBarLink": request.build_absolute_uri(
                        "/manager/couponCodes/search"
                    ),
                }
                return render(request, "chewapp/ManagerCouponCodes.html", context)

            else:
                return self.DisplayError(request, error)

        except Exception as ex:
            return self.DisplayError(request, str(ex))

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/couponCodes"),
            },
        )


class SearchCouponCodeUI:
    def __init__(self, controller: SearchCouponCodeController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):

        try:

            searchTerm = request.GET["searchTerm"]

            if searchTerm == "":
                raise Exception("Search term cannot be empty")

            rawMenuItems, error = self.controller.SearchCouponCode(searchTerm)

            if not error:
                couponCodes = [
                    {
                        "CID": item.id,
                        "Coupon": item.code,
                        "Percent": item.discount_percent,
                        "Dollar": item.discount_dollar,
                        "MinAmt": item.min_spend,
                    }
                    for item in rawMenuItems
                ]

                context = {
                    "username": request.session.get("username", "error"),
                    "profile": "manager",
                    "tabs": getTabs(request, "Coupons"),
                    "searchBar": searchTerm,
                    "createButton": request.build_absolute_uri(
                        "/manager/couponCodes/add"
                    ),
                    "activeTab": "Coupons",
                    "couponCodes": couponCodes,
                    "searchBarHome": request.build_absolute_uri(
                        "/manager/couponCodes/search"
                    ),
                    "searchBarLink": request.build_absolute_uri(
                        "/manager/couponCodes/search"
                    ),
                }

                return render(request, "chewapp/ManagerSearchCouponCodes.html", context)

            else:
                return self.DisplayError(request, error)

        except Exception as ex:
            return redirect("/manager/couponCodes")

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/couponCodes"),
            },
        )


class DeleteCouponCodeUI:
    def __init__(self, controller: DeleteCouponCodeController):
        self.controller = controller

    @with_auth(manager=True)
    def OnSubmit(self, request, CID):
        try:
            _, error = self.controller.DeleteCouponCode(CID)

            if not error:
                return HttpResponse("Ok")
            else:
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            return self.DisplayError(request, Error(500, str(ex)))

    @with_auth(manager=True)
    def DisplayError(self, request, error: Error):
        return HttpResponse(str(error), status=error.code)


class CreateCouponCodeUI:
    def __init__(self, controller: CreateCouponCodeController):
        self.controller = controller

    @with_auth(manager=True)
    def DisplayPage(self, request):
        context = {"TitleText": "Create Coupon Code"}
        return render(request, "chewapp/ManagerAddCouponCodes.html", context)

    @with_auth(manager=True)
    def OnSubmit(self, request):

        try:

            data = QueryDict(request.body)
            Coupon = data.get("coupon")
            DiscountP = data.get("discountPercent", 0)
            DiscountV = data.get("discountValue", 0)
            MinAmt = data.get("amount", 0)

            # Call the controller to create
            _, error = self.controller.CreateCouponCode(
                Code=Coupon, Percent=DiscountP, Dollar=DiscountV, MinSpend=MinAmt
            )

            if not error:
                return redirect("/manager/couponCodes")
            else:
                return self.DisplayError(request, error)

        except Exception as ex:
            return self.DisplayError(request, Error(500, str(ex)))

    @with_auth(manager=True)
    def DisplayError(self, request, error: Error):
        return HttpResponse(str(error), status=error.code)


class ModifyCouponCodeUI:
    def __init__(
        self,
        deleteCouponCodeController: DeleteCouponCodeController,
        viewCouponCodeController: ViewCouponCodeController,
        createCouponCodeController: CreateCouponCodeController,
    ):

        self.deleteCouponCodeController = deleteCouponCodeController
        self.viewCouponCodeController = viewCouponCodeController
        self.createCouponCodeController = createCouponCodeController

    @with_auth(manager=True)
    def DisplayPage(self, request, CID):
        try:
            couponCode, error = self.viewCouponCodeController.ViewCouponCode(CID)

            if not error:
                context = {
                    "TitleText": "Modify Coupon Code",
                    "Coupon": couponCode.code,
                    "MinAmt": couponCode.min_spend,
                    "CID": couponCode.id,
                }

                if couponCode.discount_percent == 0.0:
                    context["DiscountV"] = couponCode.discount_dollar
                else:
                    context["DiscountP"] = couponCode.discount_percent

                return render(request, "chewapp/ManagerModifyCouponCodes.html", context)

            else:
                return self.DisplayError(request, error)

        except Exception as ex:
            return self.DisplayError(request, str(ex))

    @with_auth(manager=True)
    def OnSubmit(self, request, CID):
        try:
            data = json.loads(request.body)

            CID = data.get("CID")
            Coupon = data.get("Coupon")
            DiscountType = data.get("DiscountType", None)
            DiscountNumber = data.get("DiscountNumber", 0)
            MinAmt = data.get("MinAmt", 0)

            if MinAmt.strip() == "":
                MinAmt = 0

            if DiscountType == "DiscountIsValue":
                DiscountP = 0.0
                DiscountV = DiscountNumber
            else:
                DiscountP = DiscountNumber
                DiscountV = 0.0

            _, error = self.createCouponCodeController.CreateCouponCode(
                Code=Coupon, Percent=DiscountP, Dollar=DiscountV, MinSpend=MinAmt
            )

            if not error:
                return HttpResponse("ok")
            else:
                return HttpResponse(str(error), status=500)

        except Exception as ex:
            return HttpResponse(str(ex), status=500)

    @with_auth(manager=True)
    def DisplayError(self, request, error):

        return render(
            request,
            "chewapp/ManagerErrorMsg.html",
            {
                "ErrorMsg": str(error),
                "TitleText": "ERROR",
                "HomeLink": request.build_absolute_uri("/manager/couponCodes"),
            },
        )
