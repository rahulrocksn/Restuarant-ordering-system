from enum import IntEnum
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    name = models.CharField(max_length=255)

    is_manager = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"UserProfile {self.name} (manager: {self.is_manager}, admin: {self.is_administrator}, owner: {self.is_owner}, staff: {self.is_staff})"

    @classmethod
    def GetByID(self, id):
        return UserProfile.objects.get(id=id)

    @classmethod
    def GetAll(self):
        return UserProfile.objects.all()

    @classmethod
    def SearchUserProfiles(self, keyword):
        return UserProfile.objects.filter(name__contains=keyword)


class Account(models.Model):
    """
    Account adds additional information to Django's built-in User model.
    https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#extending-the-existing-user-model
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_suspended = models.BooleanField(default=False)
    profile = models.ForeignKey(
        UserProfile, on_delete=models.RESTRICT, related_name="accounts"
    )

    @classmethod
    def GetByUsername(self, username):
        return Account.objects.get(user__username=username)

    @classmethod
    def GetByUserID(self, id):
        return Account.objects.get(user__id=id)

    @classmethod
    def SearchUsers(self, username):
        return Account.objects.filter(user__username__icontains=username)

    def Suspend(self):
        self.is_suspended = True
        return self

    def Unsuspend(self):
        self.is_suspended = False
        return self


class CouponCode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    code = models.CharField(max_length=32, unique=True)
    discount_percent = models.FloatField()
    discount_dollar = models.FloatField()
    min_spend = models.FloatField()

    @classmethod
    def GetAll(self):
        return CouponCode.objects.all()

    @classmethod
    def SearchKey(self, key):
        return CouponCode.objects.filter(code__icontains=key)


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=65535)
    menuItem = models.ManyToManyField("MenuItem", related_name="categories")

    @classmethod
    def GetAll(self):
        return Category.objects.all()

    @classmethod
    def SearchKey(self, key):
        return Category.objects.filter(name__icontains=key)

    @classmethod
    def GetMenuItemsFromCategory(self, id):
        return MenuItem.objects.filter(categories__id=id)


class MenuItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=65535)
    price = models.FloatField()
    stock = models.BooleanField(default=False)
    imgName = models.CharField(max_length=100, default="")
    menuImg = models.ImageField(
        upload_to="static/",
        default="static/chewapp/static/chewapp/FoodImages/testing.jpg",
    )

    @classmethod
    def GetAll(self):
        return MenuItem.objects.all()

    @classmethod
    def SearchKey(self, key):
        return MenuItem.objects.filter(name__icontains=key)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    table_no = models.IntegerField()
    total_price = models.FloatField(default=0)
    email = models.CharField(max_length=255)
    coupon = models.ForeignKey(
        CouponCode, on_delete=models.SET_NULL, null=True, related_name="+"
    )

    @classmethod
    def GetAll(self):
        return Cart.objects.all()


class CartItem(models.Model):
    """
    CartItem should include a copy of the MenuItem to keep historical integrity.
    """

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=65535)
    price = models.FloatField()
    qty = models.IntegerField(default=0)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    @classmethod
    def GetAll(self):
        return CartItem.objects.all()


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    table_no = models.IntegerField()
    total_price = models.FloatField()
    email = models.CharField(max_length=255)
    payment_reference = models.TextField(null=True)
    coupon = models.ForeignKey(
        CouponCode, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    payment_reference = models.CharField(max_length=255, default="")
    is_completed = models.BooleanField(default=False)

    @classmethod
    def GetAll(self):
        return Order.objects.all()

    @classmethod
    def GetByTable(self, table_no):
        return Order.objects.filter(table_no=table_no)

    @classmethod
    def GetByID(self, id):
        return Order.objects.get(id=id)


class OrderStatus(IntEnum):
    PLACED = 1
    PREPARING = 2
    READY = 3
    COMPLETE = 4
    CANCELLED = 5


class OrderItem(models.Model):
    """
    OrderItem should include a copy of the CartItem to keep historical integrity.
    """

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=65535)
    price = models.FloatField()
    qty = models.IntegerField(default=0)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    status = models.IntegerField(default=OrderStatus.PLACED)

    @classmethod
    def GetAll(self):
        return OrderItem.objects.all()

    @classmethod
    def GetByID(self, id):
        return OrderItem.objects.get(id=id)
