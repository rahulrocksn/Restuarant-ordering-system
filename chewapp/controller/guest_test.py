from django.test import TestCase
from .guest import (
    SubmitCartController,
    InputTableAndEmailController,
    AddToCartController,
    SubmitCartController,
)
from ..models import MenuItem, Category, CouponCode, Cart, CartItem, Order


class TestGuestController(TestCase):
    def setUp(self):
        pass

    def test_cart(self):
        # Create dummy cart and items
        cart, err = InputTableAndEmailController().InputTableAndEmail(
            123, "test@localhost"
        )
        self.assertIsNone(err)
        mi = MenuItem(name="test123", description="test item", price=123, stock=True)
        mi.save()

        # Add to cart
        items, err = AddToCartController().AddItem(mi.id, cart.id)
        self.assertIsNone(err)
        self.assertEqual(len(items), 1)

        # Submit cart to order
        order, err = SubmitCartController().SubmitOrder(cart.id, "payment")
        self.assertIsNone(err)
        self.assertEqual(len(order.items.all()), 1)
