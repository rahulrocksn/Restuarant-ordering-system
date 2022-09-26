from typing import List
from ..common.error import Result, Error
from ..models import Order, OrderItem, OrderStatus
from django.db import transaction


class ViewCustomerOrdersController:
    def GetByTable(self, TableNo) -> Result[List[Order]]:
        try:
            return Order.GetByTable(TableNo), None
        except Exception as ex:
            return None, Error(500, str(ex))


class ViewSingleOrderController:
    def GetByID(self, OrderID) -> Result[Order]:
        try:
            return Order.GetByID(OrderID), None
        except Exception as ex:
            return None, Error(500, str(ex))


class ViewAllOrdersController:
    def GetAllOrders(self) -> Result[List[Order]]:
        try:
            return Order.GetAll(), None
        except Exception as ex:
            return None, Error(500, str(ex))


class ViewOrdersByStatusController:
    def _classify_order(self, order) -> OrderStatus:
        n_placed = 0
        n_preparing = 0
        n_ready = 0
        n_complete = 0

        for item in order.items.all():
            if item.status == OrderStatus.PLACED:
                n_placed += 1
            elif item.status == OrderStatus.PREPARING:
                n_preparing += 1
            elif item.status == OrderStatus.READY:
                n_ready += 1
            elif (
                item.status == OrderStatus.COMPLETE
                or item.status == OrderStatus.CANCELLED
            ):
                n_complete += 1

        if n_placed > 0 and n_preparing == 0 and n_ready == 0 and n_complete == 0:
            return OrderStatus.PLACED
        elif n_ready > 0:
            return OrderStatus.READY
        elif n_preparing > 0:
            return OrderStatus.PREPARING
        elif n_complete > 0:
            return OrderStatus.COMPLETE

        return OrderStatus.CANCELLED

    def GetByStatus(self, status) -> Result[List[Order]]:
        try:
            if status == OrderStatus.COMPLETE:
                return Order.objects.filter(is_completed=True), None

            # Get all ongoing orders
            orders = Order.objects.filter(is_completed=False)
            results = []

            # Classify each order
            for order in orders:
                order_type = self._classify_order(order)
                if order_type == status:
                    results.append(order)

            return results, None

        except Exception as ex:
            return None, Error(500, str(ex))


class UpdateOrderController:
    def UpdateByItemID(
        self, OrderItemID, *, status=None, qty=None
    ) -> Result[OrderItem]:
        try:
            with transaction.atomic():
                orderItem = OrderItem.GetByID(OrderItemID)

                if status is not None:
                    orderItem.status = status
                if qty is not None:
                    orderItem.qty = qty

                orderItem.save()

                # Check if all orderItems in the order is completed. If so,
                # update the order to be complete.
                order = orderItem.order
                is_completed = True
                for item in order.items.all():
                    if (
                        item.status == OrderStatus.COMPLETE
                        or item.status == OrderStatus.CANCELLED
                    ):
                        continue
                    is_completed = False
                    break

                order.is_completed = is_completed
                order.save()

                return orderItem, None
        except Exception as ex:
            return None, Error(500, str(ex))
