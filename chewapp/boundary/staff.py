from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponseRedirect
from ..common.error import Error

from chewapp.common.auth_decorator import with_auth

from datetime import datetime, timezone, timedelta

from chewapp.models import MenuItem
from .templates import getStaffTabs
from django.utils.datastructures import MultiValueDictKeyError
from chewapp.controller.staff import (
    ViewOrdersByStatusController,
    ViewSingleOrderController,
    UpdateOrderController,
)


class ViewOrdersUI:
    def __init__(self, controller: ViewOrdersByStatusController):
        self.controller = controller

    def DisplayError(self, status, Message) -> HttpResponse:
        return HttpResponse(Message, status)

    @with_auth(staff=True)
    def DisplayPage(self, request):
        rawOrders, error = self.controller.GetByStatus(1)
        if not error:
            orders = [
                {
                    "orderID": order.id,
                    "Number": order.id,
                    "total_price": order.total_price,
                    "table_no": order.table_no,
                    "Time": order.created_at.astimezone(
                        timezone(timedelta(hours=8))
                    ).time(),
                }
                for order in rawOrders
            ]
        else:
            self.DisplayError(500, "Something went wrong!")

        context = {
            "username": request.session.get("username", "error"),
            "profile": "staff",
            "tabs": getStaffTabs(request, "New Orders"),
            "activeTab": "New Orders",
            "searchBar": False,
            "createButton": False,
            "orders": orders,
        }
        return render(request, "chewapp/StaffViewOrders.html", context)


class ViewOrderDetailsUI:
    def __init__(self, controller: ViewSingleOrderController):
        self.controller = controller

    def DisplayError(self, status, Message) -> HttpResponse:
        return HttpResponse(Message, status)

    @with_auth(staff=True)
    def DisplayPage(self, request, orderID) -> render:

        if orderID == -1:
            return self.DisplayError(request, "Invalid Item")

        # Query from db
        order, error = self.controller.GetByID(orderID)
        if not error:
            OrderItems = [
                {
                    "MenuItemID": item.get("id"),
                    "Name": item.get("name"),
                    "Description": item.get("description"),
                    "Price": item.get("price"),
                    "Qty": item.get("qty"),
                    "Status": item.get("status"),
                }
                for item in order.items.values()
            ]
        else:
            self.DisplayError(500, "Something went wrong!")

        context = {
            "order": order,
            "orderTime": order.created_at.astimezone(
                timezone(timedelta(hours=8))
            ).time(),
            "OrderItems": OrderItems,
        }

        return render(request, "chewapp/StaffViewOrderDetails.html", context)


class ViewInProgressOrders:
    def __init__(self, controller: ViewOrdersByStatusController):
        self.controller = controller

    def DisplayError(self, status, Message) -> HttpResponse:
        return HttpResponse(Message, status)

    @with_auth(staff=True)
    def DisplayPage(self, request):
        rawOrders, error = self.controller.GetByStatus(2)
        if not error:
            ordersIP = [
                {
                    "orderID": order.id,
                    "Number": order.id,
                    "total_price": order.total_price,
                    "table_no": order.table_no,
                    "Time": order.created_at.astimezone(
                        timezone(timedelta(hours=8))
                    ).time(),
                }
                for order in rawOrders
            ]
        else:
            self.DisplayError(500, "Something went wrong!")

        context = {
            "username": request.session.get("username", "error"),
            "profile": "staff",
            "tabs": getStaffTabs(request, "In Progress"),
            "activeTab": "In Progress",
            "searchBar": False,
            "createButton": False,
            "orders": ordersIP,
        }
        return render(request, "chewapp/StaffViewOrders.html", context)


class ViewReadyOrders:
    def __init__(self, controller: ViewOrdersByStatusController):
        self.controller = controller

    def DisplayError(self, status, Message) -> HttpResponse:
        return HttpResponse(Message, status)

    @with_auth(staff=True)
    def DisplayPage(self, request):
        rawOrders, error = self.controller.GetByStatus(3)
        if not error:
            orders = [
                {
                    "orderID": order.id,
                    "Number": order.id,
                    "total_price": order.total_price,
                    "table_no": order.table_no,
                    "Time": order.created_at.astimezone(
                        timezone(timedelta(hours=8))
                    ).time(),
                }
                for order in rawOrders
            ]
        else:
            self.DisplayError(500, "Something went wrong!")

        context = {
            "username": request.session.get("username", "error"),
            "profile": "staff",
            "tabs": getStaffTabs(request, "Ready"),
            "activeTab": "Ready",
            "searchBar": False,
            "createButton": False,
            "orders": orders,
        }
        return render(request, "chewapp/StaffViewOrders.html", context)


class ViewCompletedOrders:
    def __init__(self, controller):
        self.controller = controller

    def DisplayError(self, status, Message) -> HttpResponse:
        return HttpResponse(Message, status)

    @with_auth(staff=True)
    def DisplayPage(self, request):
        rawOrders, error = self.controller.GetByStatus(4)
        if not error:
            orders = [
                {
                    "orderID": order.id,
                    "Number": order.id,
                    "total_price": order.total_price,
                    "table_no": order.table_no,
                    "Time": order.created_at.astimezone(
                        timezone(timedelta(hours=8))
                    ).time(),
                }
                for order in rawOrders
            ]
        else:
            self.DisplayError(500, "Something went wrong!")

        context = {
            "username": request.session.get("username", "error"),
            "profile": "staff",
            "tabs": getStaffTabs(request, "Completed"),
            "activeTab": "Completed",
            "searchBar": False,
            "createButton": False,
            "orders": orders,
        }
        return render(request, "chewapp/StaffViewOrders.html", context)


class UpdateOrderDetailUI:
    def __init__(self, controller: UpdateOrderController):
        self.controller = controller

    def DisplayError(self, request, Message) -> HttpResponse:
        return HttpResponse(Message, status=405)

    @with_auth(staff=True)
    def Update(self, request) -> render:
        item_id = int(request.POST["item_id"])
        step = int(request.POST["step"])

        if item_id == -1:
            return self.DisplayError(request, "Invalid order")

        # Advance the step
        if step not in [1, 2, 3, 4, 5]:
            return self.DisplayError(request, "Invalid status")

        _, err = self.controller.UpdateByItemID(item_id, status=step)
        if err is not None:
            return self.DisplayError(request, "Error: " + str(err))

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UpdateOrderQty:
    def __init__(self, controller: UpdateOrderController):
        self.controller = controller

    def DisplayError(self, request, Message) -> HttpResponse:
        return HttpResponse(Message, status=405)

    @with_auth(staff=True)
    def Update(self, request) -> render:
        item_id = int(request.POST["item_id"])
        qty = int(request.POST["qty"])
        operation = request.POST["operation"]

        if operation == "add":
            qty += 1
        else:
            qty -= 1

        if item_id == -1:
            return self.DisplayError(request, "Invalid order")

        # Change the status
        if qty < 0:
            return self.DisplayError(request, "Invalid quantity")

        if qty == 0:
            _, err = self.controller.UpdateByItemID(item_id, status=5)
            if err is not None:
                return self.DisplayError(request, "Error: " + str(err))

        _, err = self.controller.UpdateByItemID(item_id, qty=qty)
        if err is not None:
            return self.DisplayError(request, "Error: " + str(err))

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
