from django.test import TestCase
from ..models import OrderStatus, Order, OrderItem
from .staff import ViewOrdersByStatusController


class TestStaff(TestCase):
    def setUp(self):
        pass

    def test_order_classification(self):
        c = ViewOrdersByStatusController()

        # Create mock order and order items
        def make_order(statuses):
            order = Order(
                table_no=123,
                total_price=5,
                email="someone@localhost",
                is_completed=False,
            )
            order.save()
            for status in statuses:
                item = OrderItem(
                    name="test item",
                    description="testing 123",
                    price=1,
                    order=order,
                    status=status,
                )
                item.save()
            return order

        self.assertEqual(
            c._classify_order(make_order([OrderStatus.PLACED, OrderStatus.PLACED])),
            OrderStatus.PLACED,
        )
        self.assertEqual(
            c._classify_order(make_order([OrderStatus.PREPARING, OrderStatus.PLACED])),
            OrderStatus.PREPARING,
        )
        self.assertEqual(
            c._classify_order(make_order([OrderStatus.PREPARING, OrderStatus.READY])),
            OrderStatus.READY,
        )
        self.assertEqual(
            c._classify_order(make_order([OrderStatus.PLACED, OrderStatus.READY])),
            OrderStatus.READY,
        )
        self.assertEqual(
            c._classify_order(make_order([OrderStatus.COMPLETE, OrderStatus.READY])),
            OrderStatus.READY,
        )

        orders, err = c.GetByStatus(OrderStatus.PLACED)
        self.assertIsNone(err)
        self.assertEqual(len(orders), 1)

        orders, err = c.GetByStatus(OrderStatus.PREPARING)
        self.assertIsNone(err)
        self.assertEqual(len(orders), 1)

        orders, err = c.GetByStatus(OrderStatus.READY)
        self.assertIsNone(err)
        self.assertEqual(len(orders), 3)
