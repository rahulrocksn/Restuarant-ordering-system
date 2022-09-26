from typing import List
from django.shortcuts import redirect, render, HttpResponse
from django.http import QueryDict

from chewapp.controller.guest import (
    AddToCartController,
    ApplyCouponController,
    BrowseMenuController,
    GetCartItemsController,
    GetCouponsController,
    InputTableAndEmailController,
    MenuCategoryController,
    MenuSearchController,
    ModifyCartController,
    SubmitCartController,
)
from chewapp.controller.manager import SearchCategoryController, ViewMenuController
from chewapp.models import MenuItem
from .templates import getTabs
from django.utils.datastructures import MultiValueDictKeyError
from ..common.error import Error
import json


class InputTableAndEmailUI:
    def __init__(self, controller: InputTableAndEmailController):
        self.controller = controller

    def DisplayPage(self, request) -> render:

        # Check if Table No is passed into get. If not, leave empty
        try:
            Table = int(request.GET["table"])
        except MultiValueDictKeyError:
            Table = request.session.get("Table", "")
        except ValueError:
            Table = ""

        Email = request.session.get("Email", "")

        context = {"Table": Table, "Email": Email, "Title": "Chewsters - Select Table"}

        return render(request, "chewapp/GuestGetTableEmail.html", context)

    def OnSubmit(self, request) -> redirect:
        Table = request.POST["Table"]
        Email = request.POST["Email"]

        request.session["Table"] = Table
        request.session["Email"] = Email

        # Get ID from controller
        Cart, CartError = self.controller.InputTableAndEmail(Table, Email)

        if not CartError:
            request.session["CartID"] = Cart.id

            return redirect("guestMenu")
        else:
            return redirect("guestTableNo")


class BrowseMenuUI:
    def __init__(
        self,
        searchCategoryController: SearchCategoryController,
        menuCategoryController: MenuCategoryController,
        browseMenuController: BrowseMenuController,
        getCartItemsController: GetCartItemsController,
    ):
        self.searchCategoryController = searchCategoryController
        self.menuCategoryController = menuCategoryController
        self.browseMenuController = browseMenuController
        self.getCartItemsController = getCartItemsController

    def DisplayPage(self, request) -> render:

        try:
            if (
                (request.session.get("Table") is None)
                or (request.session.get("Email") is None)
                or (request.session.get("CartID") is None)
            ):
                return redirect("guestTableNo")

            selectedCat = request.GET.get("catID", "-1")
            #! have range check here to ensure that it's fine. Probably have a const file somewhere to declare ranges

            # Get all catagories
            RAWcategories, CatError = self.searchCategoryController.SearchCategory("")

            if CatError is not None:
                return self.DisplayError(request, CatError)

            Categories = [{"CategoryID": -1, "Name": "All"}] + [
                {"CategoryID": category.id, "Name": category.name}
                for category in RAWcategories
            ]

            selectedCat = int(selectedCat)

            # Get menu items
            if selectedCat == -1:  # None selected
                RAWItems, MenuError = self.browseMenuController.BrowseMenuItem()
            else:  # Get via category
                RAWItems, MenuError = self.menuCategoryController.GetMenuItems(
                    selectedCat
                )

            if MenuError is not None:
                return self.DisplayError(request, MenuError)

            Items = [
                {
                    "MenuItemID": item.id,
                    "Name": item.name,
                    "Price": item.price,
                    "Description": item.description,
                    "Image": item.menuImg.url,
                    "IsAvailable": item.stock,
                }
                for item in RAWItems
            ]

            # Get Cart Size
            CartID = request.session.get("CartID")
            CartItems, CartItemError = self.getCartItemsController.GetCart(CartID)

            if CartItemError is not None:
                return self.DisplayError(request, CartItemError)

            CartSize = 0

            for CartItem in CartItems:
                CartSize += CartItem.qty

            context = {
                "Categories": Categories,
                "ItemsInSelectedCategory": Items,
                "CartSize": CartSize,
                "SelectedCategoryID": selectedCat,
                "TableNo": request.session["Table"],
                "SearchBarLink": request.build_absolute_uri("/search"),
                "CartLink": request.build_absolute_uri("/cart"),
                "AtMainMenu": True,
                "Title": "Chewsters - Menu",
            }

            return render(request, "chewapp/GuestViewMenu.html", context)

        except (KeyError, ValueError, MultiValueDictKeyError):
            return redirect("guestTableNo")

    def DisplayError(self, request, Message: Error) -> render:
        return render(
            request,
            "chewapp/GuestErrorView.html",
            {"errorMsg": Message, "TableNo": request.session.get("Table")},
        )


class BrowseMenuSearchUI:
    def __init__(
        self,
        menuSearchController: MenuSearchController,
        getCartItemsController: GetCartItemsController,
    ):
        self.menuSearchController = menuSearchController
        self.getCartItemsController = getCartItemsController

    def DisplayPage(self, request) -> render:

        try:
            if (
                (request.session.get("Table") is None)
                or (request.session.get("Email") is None)
                or (request.session.get("CartID") is None)
            ):
                return redirect("guestTableNo")

            try:
                if len(str(request.GET.get("Keyword", "")).strip()) == 0:
                    return redirect("guestMenu")
            except MultiValueDictKeyError:
                return redirect("guestMenu")

            # Get the menu items from the controller.
            # menuItems, Error = self.GetMenuItems(self, catagory)

            SearchTerm = str(request.GET.get("Keyword", ""))

            RAWMenuItems, MenuError = self.menuSearchController.GetMenuItems(SearchTerm)

            if MenuError is not None:
                return self.DisplayError(request, str(MenuError))

            FoodItems = [
                {
                    "MenuItemID": item.id,
                    "Name": item.name,
                    "Price": item.price,
                    "Description": item.description,
                    "Image": item.menuImg.url,
                    "IsAvailable": item.stock,
                }
                for item in RAWMenuItems
            ]

            # Refresh Cart Size

            CartID = request.session.get("CartID")
            CartItems, CartItemError = self.getCartItemsController.GetCart(CartID)

            if CartItemError is not None:
                return self.DisplayError(request, str(CartItemError))

            CartSize = 0

            for CartItem in CartItems:
                CartSize += CartItem.qty

            return self.DisplayMenuItems(request, FoodItems, CartSize)

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, str(E))

    def DisplayMenuItems(
        self, request, FoodItems: List[MenuItem], CartSize: int
    ) -> render:

        try:
            context = {
                "FoodItems": FoodItems,
                "TableNo": request.session["Table"],
                "CartSize": CartSize,
                "SearchBarLink": request.build_absolute_uri("/search"),
                "SearchTerm": request.GET["Keyword"],
                "CartLink": request.build_absolute_uri("/cart"),
                "Title": "Chewsters - Menu",
            }

            return render(request, "chewapp/GuestViewMenuSearch.html", context)

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, str(E))

    def DisplayError(self, request, Message: Error) -> render:
        context = {
            "ErrorMsg": Message,
            "TableNo": request.session["Table"],
            "Title": "Chewsters - Menu",
        }

        return render(request, "chewapp/GuestViewMenuItem.html", context)


class BrowseMenuItemUI:
    def __init__(
        self,
        viewMenuController: ViewMenuController,
        getCartItemsController: GetCartItemsController,
    ):
        self.viewMenuController = viewMenuController
        self.getCartItemsController = getCartItemsController

    def DisplayPage(self, request, MenuItemID: int) -> render:

        try:
            if (request.session.get("Table") is None) or (
                request.session.get("Email") is None
                or (request.session.get("CartID") is None)
            ):
                return redirect("guestTableNo")

            # Get cart size
            CartID = request.session.get("CartID")
            CartItems, CartItemError = self.getCartItemsController.GetCart(CartID)

            if CartItemError is not None:
                return self.DisplayError(request, str(CartItemError))

            CartSize = 0

            for CartItem in CartItems:
                CartSize += CartItem.qty

            # Get the menu item from the controller.
            RAWMenuItem, MenuError = self.viewMenuController.ViewMI(MenuItemID)

            if MenuError is not None:
                return self.DisplayError(request, str(MenuError))

            MenuItem = {
                "MenuItemID": RAWMenuItem.id,
                "Name": RAWMenuItem.name,
                "Price": RAWMenuItem.price,
                "Description": RAWMenuItem.description,
                "Image": RAWMenuItem.menuImg.url,
                "IsAvailable": RAWMenuItem.stock,
            }

            context = {
                "Item": MenuItem,
                "TableNo": request.session["Table"],
                "CartSize": CartSize,
                "CartLink": request.build_absolute_uri("/cart"),
                "Title": "Chewsters - Menu",
            }

            return render(request, "chewapp/GuestViewMenuItem.html", context)

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, str(E))

    def DisplayError(self, request, Message: Error) -> render:
        context = {
            "ErrorMsg": Message,
            "TableNo": request.session["Table"],
            "Title": "Chewsters - ERROR",
        }

        return render(request, "chewapp/GuestViewMenuItem.html", context)


class AddToCartUI:
    def __init__(self, addToCartController: AddToCartController):
        self.addToCartController = addToCartController

    def OnSubmit(self, request) -> HttpResponse:

        try:
            CartID = request.session.get("CartID")

            data = json.loads(request.body)

            ItemID = data.get("id")

            _, AddToCartError = self.addToCartController.AddItem(ItemID, CartID)

            if AddToCartError is not None:
                return self.DisplayError(request, str(AddToCartError))

            return self.DisplayCartItems(request)

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return HttpResponse(str(E), status=405)

    def DisplayCartItems(self, request) -> HttpResponse:
        return HttpResponse("ok")

    def DisplayError(self, request, Message: Error) -> HttpResponse:
        return HttpResponse(status=405)


class ModifyCartUI:
    def __init__(
        self,
        modifyCartController: ModifyCartController,
        getCartItemsController: GetCartItemsController,
    ):
        self.modifyCartController = modifyCartController
        self.getCartItemsController = getCartItemsController

    def DisplayPage(self, request) -> render:

        try:
            if (
                (request.session.get("Table") is None)
                or (request.session.get("Email") is None)
                or (request.session.get("CartID") is None)
            ):
                return redirect("guestTableNo")

            TotalPrice = 0
            Qty = 0

            CartID = request.session.get("CartID")

            RAWCartItems, CartItemError = self.getCartItemsController.GetCart(CartID)

            if CartItemError is not None:
                return self.DisplayError(request, str(CartItemError))

            CartItems = [
                {
                    "CartItemID": item.id,
                    "MenuItemID": item.menu_item.id,
                    "Name": item.name,
                    "Price": item.price,
                    "Description": item.description,
                    "Qty": item.qty,
                }
                for item in RAWCartItems
            ]

            for entry in CartItems:
                TotalPrice += float(entry["Price"]) * float(entry["Qty"])
                Qty += int(entry["Qty"])

            context = {
                "TableNo": request.session["Table"],
                "CartSize": Qty,
                "CartItems": CartItems,
                "TotalPrice": TotalPrice,
                "BackLink": request.build_absolute_uri("/"),
                "Title": "Chewsters - Cart",
            }

            return render(request, "chewapp/GuestViewCart.html", context)

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, Error(500, str(E)))

    def OnSubmit(self, request) -> HttpResponse:

        try:
            data = json.loads(request.body)
            id = data.get("id")
            qty = data.get("qty")

            _, ModifyError = self.modifyCartController.ModifyItem(id, qty)

            if ModifyError is not None:
                return self.DisplayError(request, ModifyError)

            return self.DisplayCartItems(request)

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, Error(500, str(E)))

    def DisplayCartItems(self, request) -> HttpResponse:

        return HttpResponse("ok")

    def DisplayError(self, request, Message: Error) -> render:
        context = {
            "ErrorMsg": Message,
            "TableNo": request.session["Table"],
            "Title": "Chewsters - ERROR",
        }

        return HttpResponse(Message, status=405)


class SubmitCartUI:
    def __init__(
        self,
        getCartItemsController: GetCartItemsController,
        getCouponsController: GetCouponsController,
        applyCouponController: ApplyCouponController,
        submitCartController: SubmitCartController,
        inputTableAndEmailController: InputTableAndEmailController,
    ):
        self.getCartItemsController = getCartItemsController
        self.getCouponsController = getCouponsController
        self.applyCouponController = applyCouponController
        self.submitCartController = submitCartController
        self.inputTableAndEmailController = inputTableAndEmailController

    def DisplayPage(self, request) -> render:

        try:
            if (request.session.get("Table") is None) or (
                request.session.get("Email") is None
            ):
                return redirect("guestTableNo")

            # Code to get cart details (to get total)
            Cart, CartError = self.getCartItemsController.GetCart(
                request.session["CartID"]
            )

            if CartError is not None:
                self.DisplayError(request, CartError)

            TotalPrice = 0
            CartSize = 0
            for item in Cart:
                TotalPrice += float(item.price) * float(item.qty)
                CartSize += item.qty

            if CartSize == 0:
                self.DisplayError(request, Error(500, "Cart is empty"))

            # Code to get coupons
            RAWCoupons, CouponError = self.getCouponsController.GetCoupons()

            if CouponError is not None:
                self.DisplayError(request, CouponError)

            CouponList = [
                {
                    "CouponID": coupon.id,
                    "code": coupon.code,
                    "discount_dollar": coupon.discount_dollar,
                    "discount_percent": coupon.discount_percent,
                    "min_spend": coupon.min_spend,
                }
                for coupon in RAWCoupons
            ]

            context = {
                "TableNo": request.session["Table"],
                "CartSize": CartSize,
                "TotalPrice": TotalPrice,
                "Coupons": CouponList,
                "Title": "Chewsters - Checkout",
            }

            return render(request, "chewapp/GuestCheckout.html", context)

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, Error(500, str(E)))

    def OnSubmit(self, request) -> HttpResponse:

        try:
            CartID = request.session["CartID"]
            CreditCardNumber = request.POST.get("CreditCardNumber")
            CreditCardName = request.POST.get("CreditCardName")
            CreditCardExpiryMonth = request.POST.get("CreditCardExpiryMonth")
            CreditCardExpiryYear = request.POST.get("CreditCardExpiryYear")
            CreditCardCVC = request.POST.get("CreditCardCVC")

            data = {
                "CreditCardNumber": CreditCardNumber,
                "CreditCardName": CreditCardName,
                "CreditCardExpiryMonth": CreditCardExpiryMonth,
                "CreditCardExpiryYear": CreditCardExpiryYear,
                "CreditCardCVC": CreditCardCVC,
            }

            dataJSON = json.dumps(data)

            Order, OrderError = self.submitCartController.SubmitOrder(CartID, dataJSON)

            if OrderError is not None:
                return self.DisplayError(request, OrderError)

            TableNo = request.session["Table"]
            Email = request.session["Email"]
            (
                NewCart,
                NewCartError,
            ) = self.inputTableAndEmailController.InputTableAndEmail(TableNo, Email)

            if NewCartError is not None:
                return self.DisplayError(request, NewCartError)

            request.session["CartID"] = NewCart.id

            return render(request, "chewapp/GuestConfirmCart.html")

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, Error(500, str(E)))

    def SetCouponCode(self, request) -> HttpResponse:

        try:
            CartID = request.session["CartID"]

            CouponCode = json.loads(request.body).get("CouponCode")

            NewTotal, CouponError = self.applyCouponController.GetUpdatedPrice(
                CartID, CouponCode
            )

            if CouponError is not None:
                return HttpResponse(status=405)

            return HttpResponse(
                json.dumps({"total": NewTotal}), content_type="application/json"
            )

        except (KeyError, ValueError, MultiValueDictKeyError) as E:
            return self.DisplayError(request, Error(500, str(E)))

    def RemoveCouponCode(self, request) -> HttpResponse:

        CartID = request.session["CartID"]

        NewTotal, CouponError = self.applyCouponController.GetUpdatedPrice(CartID, "")

        if CouponError is not None:
            return HttpResponse(status=405)

        return HttpResponse(
            json.dumps({"total": NewTotal}), content_type="application/json"
        )

    def DisplayError(self, request, Message: Error) -> render:
        context = {
            "errorMsg": str(Message),
            "TableNo": request.session["Table"],
            "Title": "Chewsters - ERROR",
        }

        return render(request, "chewapp/GuestErrorView.html", context)
