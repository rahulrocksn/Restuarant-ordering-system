from django.test import TestCase
from ..models import OrderStatus, Order, OrderItem, MenuItem
from .owner import (
    AnalyticsVisitsYearController,
    AnalyticsDollarsSpentYearController,
)
from datetime import datetime, timezone

# Raise error on timezone warnings
import warnings

warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)


class TestOwner(TestCase):
    def setUp(self):
        menu_items = [
            MenuItem(
                name=f"test menu item {i}",
                description="test",
                price=1,
                stock=True,
            )
            for i in range(3)
        ]
        for i in menu_items:
            i.save()

        for o in range(12):
            order = Order(
                table_no=123,
                total_price=10,
                email="someone@localhost",
                is_completed=True,
            )
            order.save()

            # Override the created_at timestamp
            Order.objects.filter(id=order.id).update(
                created_at=datetime(2021, o + 1, 15, tzinfo=timezone.utc)
            )

            for i in range(10):
                item = OrderItem(
                    name=f"test item {i} for order {o}",
                    description="testing 123",
                    price=1,
                    order=order,
                    status=OrderStatus.COMPLETE,
                    menu_item=menu_items[i % 3],
                )
                item.save()

    def test_visits(self):
        res, err = AnalyticsVisitsYearController().AnalyticsVisitsYear(2021)
        self.assertIsNone(err)
        self.assertEqual(len(res), 12)
        for i in res:
            self.assertEqual(i, 1)

    def test_dollars(self):
        res, err = AnalyticsDollarsSpentYearController().AnalyticsDollarsSpentYear(2021)
        self.assertIsNone(err)
        self.assertEqual(len(res), 12)
        for i in res:
            self.assertEqual(i, 10)
