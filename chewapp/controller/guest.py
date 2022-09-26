from typing import List
from ..common.error import Result, Error
from ..models import (
    MenuItem,
    Category,
    CouponCode,
    Cart,
    CartItem,
    Order,
    OrderItem,
    OrderStatus,
)
from django.db import transaction


class MenuCategoryController:
    def __init__(self):
        pass

    def GetMenuItems(self, CategoryID) -> Result[List[MenuItem]]:
        try:
            return Category.GetMenuItemsFromCategory(id=CategoryID), None
        except Exception as ex:
            return None, Error(500, "Failed to get:" + str(ex))


class MenuSearchController:
    def __init__(self):
        pass

    def GetMenuItems(self, keyword) -> Result[List[MenuItem]]:
        try:
            return MenuItem.SearchKey(keyword), None
        except Exception as ex:
            return None, Error(500, "Failed to search:" + str(ex))


class BrowseMenuController:
    def __init__(self):
        pass

    def BrowseMenuItem(self):
        try:
            return MenuItem.GetAll(), None
        except Exception as ex:
            return None, Error(500, "Failed to browse:" + str(ex))


class AddToCartController:
    def __init__(self):
        pass

    def AddItem(self, MIID, CartID) -> Result[List[CartItem]]:
        try:
            menu = MenuItem.objects.get(id=MIID)
            c = Cart.objects.get(id=CartID)

            # Check if the item is already in the cart
            cartItem = CartItem.objects.filter(cart=c, menu_item=menu)
            if len(cartItem) == 0:
                newCartItem = CartItem(
                    name=menu.name,
                    description=menu.description,
                    price=menu.price,
                    menu_item=menu,
                    cart=c,
                    qty=1,
                )
                newCartItem.save()
            else:
                cartItem[0].qty += 1
                cartItem[0].save()

            items = CartItem.objects.filter(cart_id=CartID)
            return items, None
        except Exception as ex:
            return None, Error(500, "Failed to add to cart:" + str(ex))


class ModifyCartController:
    def __init__(self):
        pass

    def ModifyItem(self, CartItemID, Qty) -> Result[List[CartItem]]:
        try:
            cartItem = CartItem.objects.get(id=CartItemID)
            if Qty > 0:
                cartItem.qty = Qty
                cartItem.save()
                return CartItem.objects.filter(cart_id=cartItem.cart_id), None

            elif Qty == 0:
                cartItem.delete()
                return CartItem.objects.filter(cart_id=cartItem.cart_id), None

        except Exception as ex:
            return None, Error(500, "Failed to modify cart:" + str(ex))


class GetCartItemsController:
    def __init__(self):
        pass

    def GetCart(self, CartID) -> Result[List[CartItem]]:
        try:
            return CartItem.objects.filter(cart_id=CartID), None
        except Exception as ex:
            return None, Error(500, "Failed to get cart:" + str(ex))


class ApplyCouponController:
    def __init__(self):
        pass

    def GetUpdatedPrice(self, CartID, CCode) -> Result[float]:
        try:
            with transaction.atomic():
                c = Cart.objects.get(id=CartID)
                ci = CartItem.objects.filter(cart_id=c.id)

                subTotal = 0.0

                for i in ci:
                    subTotal += i.price * i.qty

                total = 0.0

                if CCode == "" or CCode is None:
                    # if coupon not applicable returns subtotal as total
                    c.total_price = subTotal
                    c.save()
                    return subTotal, None

                else:
                    code = CouponCode.objects.get(code=CCode)

                    # applies discount in terms of dollars
                    if code.discount_percent == 0.0 and subTotal >= code.min_spend:
                        total = subTotal - code.discount_dollar
                        c.total_price = total
                        c.coupon_id = code.id
                        c.save()
                        return total, None

                    # applies discount in terms of percentage
                    elif code.discount_dollar == 0.0 and subTotal >= code.min_spend:
                        total = subTotal - (subTotal * (code.discount_percent / 100))
                        total = round(total, 2)
                        c.total_price = total
                        c.coupon_id = code.id
                        c.save()
                        return total, None

                    return subTotal, None

        except Exception as ex:
            return None, Error(500, "Failed to apply coupon:" + str(ex))


class GetCouponsController:
    def __init__(self):
        pass

    def GetCoupons(self) -> Result[List[CouponCode]]:
        try:
            return CouponCode.GetAll(), None
        except Exception as ex:
            return None, Error(500, "Failed to get coupons:" + str(ex))


class SubmitCartController:
    def __init__(self):
        pass

    def SubmitOrder(self, CartID, PaymentRef) -> Result[Order]:
        try:
            with transaction.atomic():

                c = Cart.objects.get(id=CartID)

                ci = CartItem.objects.filter(cart_id=c.id)

                subTotal = 0.0

                for i in ci:
                    subTotal += i.price * i.qty

                if c.coupon is not None:
                    coupon = c.coupon
                    code = CouponCode.objects.get(id=coupon.id)

                    if code.discount_percent == 0.0 and subTotal >= code.min_spend:
                        subTotal = subTotal - code.discount_dollar
                        c.total_price = subTotal
                        c.save()
                    else:
                        subTotal = subTotal - (subTotal * (code.discount_percent / 100))
                        c.total_price = round(subTotal, 2)
                        c.save()

                order = Order(
                    table_no=c.table_no,
                    total_price=subTotal,
                    email=c.email,
                    payment_reference=PaymentRef,
                    coupon=c.coupon,
                )
                order.save()

                # Transfer items from cart to order
                for item in c.items.all():
                    orderItem = OrderItem(
                        name=item.name,
                        description=item.description,
                        price=item.price,
                        qty=item.qty,
                        menu_item=item.menu_item,
                        order=order,
                        status=OrderStatus.PLACED,
                    )
                    orderItem.save()

                # Delete the cart
                c.delete()
                return order, None
        except Exception as ex:
            return None, Error(500, "Failed to order:" + str(ex))


class InputTableAndEmailController:
    def __init__(self):
        pass

    def InputTableAndEmail(self, TableNum, Email) -> Result[CartItem]:
        try:
            c = Cart(table_no=TableNum, email=Email)
            c.save()
            return c, None
        except Exception as ex:
            return None, Error(500, "Failed to input table and email:" + str(ex))
