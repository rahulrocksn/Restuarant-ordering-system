from django.urls import path

from chewapp.controller.owner import (
    AnalyticsDollarsSpentMonthController,
    AnalyticsDollarsSpentWeekController,
    AnalyticsDollarsSpentYearController,
    AnalyticsLengthBetweenCustomerVisitsController,
    AnalyticsMenuItemsFrequencyTotalController,
    AnalyticsVisitsMonthController,
    AnalyticsVisitsWeekController,
    AnalyticsVisitsYearController,
)


from .common.method_router import route
from .controller.sample import SampleController
from .controller.auth import LoginController
from .boundary.sample import SampleBoundary
from .boundary.manager import (
    AddCategoryUI,
    CreateCouponCodeUI,
    CreateMenuItemUI,
    DeleteCategoryUI,
    DeleteCouponCodeUI,
    ModifyCategoryUI,
    ModifyCouponCodeUI,
    ModifyMenuItemUI,
    SearchCategoryUI,
    SearchCouponCodeUI,
    ViewCategoryUI,
    ViewCouponCodeUI,
    ViewMenuUI,
    DeleteMenuItemUI,
    SearchMenuItemUI,
)
from .boundary.auth import LoginUI, LogoutUI
from .boundary.guest import (
    AddToCartUI,
    BrowseMenuItemUI,
    BrowseMenuSearchUI,
    InputTableAndEmailUI,
    BrowseMenuUI,
    ModifyCartUI,
    SubmitCartUI,
)
from .controller.manager import (
    ViewCategoryController,
    ViewMenuController,
    CreateNewMenuItemController,
    DeleteMenuItemController,
    SearchMenuItemController,
    ModifyMenuItemController,
    CreateCouponCodeController,
    DeleteCouponCodeController,
    SearchCouponCodeController,
    GetAllCouponCodeController,
    ViewCouponCodeController,
    AddCategoryController,
    DeleteCategoryController,
    SearchCategoryController,
    ModifyCategoryController,
)

from .controller.staff import (
    ViewOrdersByStatusController,
    ViewSingleOrderController,
    UpdateOrderController,
)

from .boundary.staff import (
    ViewOrdersUI,
    ViewOrderDetailsUI,
    ViewInProgressOrders,
    ViewReadyOrders,
    ViewCompletedOrders,
    UpdateOrderDetailUI,
    UpdateOrderQty,
)

# Admin
from .boundary.admin import (
    CreateUserAccountUI,
    CreateUserProfileUI,
    DeleteUserProfileUI,
    ModifyUserAccountUI,
    SearchUserProfilesUI,
    SearchUsersUI,
    ModifyUserProfileUI,
    SuspendUserAccountUI,
    UnsuspendUserAccountUI,
)
from .controller.admin import (
    AssignProfileController,
    CreateUserProfileController,
    DeleteUserProfileController,
    ListUserProfilesController,
    ModifyUserController,
    SearchUserProfilesController,
    SearchUsersController,
    CreateUsersController,
    SuspendUserController,
    UnsuspendUserController,
    ViewUserController,
    ViewUserProfileController,
    ModifyUserProfileController,
)

from .controller.guest import (
    BrowseMenuController,
    GetCartItemsController,
    GetCouponsController,
    MenuCategoryController,
    MenuSearchController,
    AddToCartController,
    ModifyCartController,
    ApplyCouponController,
    SubmitCartController,
    InputTableAndEmailController,
)

# Owner
from .boundary.owner import (
    AvgLength,
    DollarsSpent,
    MenuItemsFrequency,
    NumberOfVisits,
)

sample_controller = SampleController()
sample = SampleBoundary(sample_controller)


loginController = LoginController()
loginUI = LoginUI(loginController)
logoutUI = LogoutUI()


# SearchMenuItemController

# Manager
ManagerViewMenuController = ViewMenuController()
ManagerViewMenuUI = ViewMenuUI(ManagerViewMenuController)
ManagerDeleteMenuItemController = DeleteMenuItemController()
ManagerDeleteMenuItemUI = DeleteMenuItemUI(ManagerDeleteMenuItemController)
ManagerSearchMenuItemController = SearchMenuItemController()
ManagerSearchMenuItemUI = SearchMenuItemUI(ManagerSearchMenuItemController)
ManagerModifyMenuItemController = ModifyMenuItemController()
ManagerModifyMenuItemUI = ModifyMenuItemUI(
    ManagerDeleteMenuItemController,
    ManagerViewMenuController,
    ManagerModifyMenuItemController,
)
ManagerCreateNewMenuItemController = CreateNewMenuItemController()
ManagerCreateNewMenuItemUI = CreateMenuItemUI(ManagerCreateNewMenuItemController)

ManagerViewCategoryController = ViewCategoryController()
ManagerViewCategoryUI = ViewCategoryUI(ManagerViewCategoryController)
ManagerDeleteCategoryController = DeleteCategoryController()
ManagerDeleteCategoryUI = DeleteCategoryUI(ManagerDeleteCategoryController)
ManagerSearchCategoryController = SearchCategoryController()
ManagerSearchCategoryUI = SearchCategoryUI(ManagerSearchCategoryController)
ManagerAddCategoryController = AddCategoryController()
ManagerAddCategoryUI = AddCategoryUI(
    ManagerAddCategoryController, ManagerViewMenuController
)
ManagerModifyCategoryController = ModifyCategoryController()
ManagerModifyCategoryUI = ModifyCategoryUI(
    ManagerDeleteCategoryController,
    ManagerViewCategoryController,
    ManagerModifyCategoryController,
    ManagerViewMenuController,
)

ManagerViewCouponCodeController = ViewCouponCodeController()
ManagerGetAllCouponCodeController = GetAllCouponCodeController()
ManagerViewCouponCodeUI = ViewCouponCodeUI(ManagerGetAllCouponCodeController)
ManagerSearchCouponCodeController = SearchCouponCodeController()
ManagerSearchCouponCodeUI = SearchCouponCodeUI(ManagerSearchCouponCodeController)
ManagerDeleteCouponCodeController = DeleteCouponCodeController()
ManagerDeleteCouponCodeUI = DeleteCouponCodeUI(ManagerDeleteCouponCodeController)
ManagerCreateCouponCodeController = CreateCouponCodeController()
ManagerCreateCouponCodeUI = CreateCouponCodeUI(ManagerCreateCouponCodeController)

# no separate modify coupon code controller?
ManagerModifyCouponCodeUI = ModifyCouponCodeUI(
    ManagerDeleteCouponCodeController,
    ManagerViewCouponCodeController,
    ManagerCreateCouponCodeController,
)

# Guest
# ! Replace with real controller later
GuestInputTableAndEmailController = InputTableAndEmailController()
GuestInputTableAndEmailUI = InputTableAndEmailUI(GuestInputTableAndEmailController)
GuestSearchCategoryController = SearchCategoryController()
GuestMenuCategoryController = MenuCategoryController()
GuestBrowseMenuController = BrowseMenuController()
GuestGetCartItemsController = GetCartItemsController()
GuestBrowseMenuUI = BrowseMenuUI(
    GuestSearchCategoryController,
    GuestMenuCategoryController,
    GuestBrowseMenuController,
    GuestGetCartItemsController,
)
GuestMenuSearchController = MenuSearchController()
GuestBrowseMenuSearchUI = BrowseMenuSearchUI(
    GuestMenuSearchController, GuestGetCartItemsController
)
GuestViewMenuController = ViewMenuController()
GuestBrowseMenuItemUI = BrowseMenuItemUI(
    GuestViewMenuController, GuestGetCartItemsController
)
GuestAddToCartController = AddToCartController()
GuestAddToCartUI = AddToCartUI(GuestAddToCartController)
GuestModifyCartController = ModifyCartController()
GuestGetCartItemsController = GetCartItemsController()
GuestModifyCartUI = ModifyCartUI(GuestModifyCartController, GuestGetCartItemsController)
GuestGetCouponsController = GetCouponsController()
GuestApplyCouponController = ApplyCouponController()
GuestSubmitCartController = SubmitCartController()
GuestSubmitCartUI = SubmitCartUI(
    GuestGetCartItemsController,
    GuestGetCouponsController,
    GuestApplyCouponController,
    GuestSubmitCartController,
    GuestInputTableAndEmailController,
)

StaffViewOrdersByStatusController = ViewOrdersByStatusController()
StaffViewMenuUI = ViewOrdersUI(StaffViewOrdersByStatusController)
StaffViewSingleOrder = ViewSingleOrderController()
StaffViewOrderDetailsUI = ViewOrderDetailsUI(StaffViewSingleOrder)
StaffViewInProgress = ViewInProgressOrders(StaffViewOrdersByStatusController)
StaffViewReadyOrders = ViewReadyOrders(StaffViewOrdersByStatusController)
StaffViewCompletedOrders = ViewCompletedOrders(StaffViewOrdersByStatusController)
StaffUpdateOrderController = UpdateOrderController()
StaffUpdateOrderItem = UpdateOrderDetailUI(StaffUpdateOrderController)
StaffUpdateOrderQty = UpdateOrderQty(StaffUpdateOrderController)

# ADMIN
AdminSearchUsersController = SearchUsersController()
AdminSearchUsersUI = SearchUsersUI(AdminSearchUsersController)
AdminSearchUserProfilesController = SearchUserProfilesController()
AdminSearchUserProfilesUI = SearchUserProfilesUI(AdminSearchUserProfilesController)
AdminListUserProfileController = ListUserProfilesController()
AdminCreateUsersController = CreateUsersController()
AdminCreateUserAccountUI = CreateUserAccountUI(
    AdminListUserProfileController, AdminCreateUsersController
)
AdminCreateUserProfileController = CreateUserProfileController()
AdminCreateUserProfileUI = CreateUserProfileUI(AdminCreateUserProfileController)
AdminViewUserProfileController = ViewUserProfileController()
AdminModifyUserProfileController = ModifyUserProfileController()
AdminModifyUserProfileUI = ModifyUserProfileUI(
    AdminViewUserProfileController, AdminModifyUserProfileController
)
AdminSuspendUserController = SuspendUserController()
AdminSuspendUserAccountUI = SuspendUserAccountUI(AdminSuspendUserController)
AdminnUnsuspendUserController = UnsuspendUserController()
AdminUnsuspendUserAccountUI = UnsuspendUserAccountUI(AdminnUnsuspendUserController)
AdminDeleteUserProfileController = DeleteUserProfileController()
AdminDeleteUserProfileUI = DeleteUserProfileUI(AdminDeleteUserProfileController)
AdminModifyUserController = ModifyUserController()
AdminAssignProfileController = AssignProfileController()
AdminViewUserController = ViewUserController()
AdminModifyUserUI = ModifyUserAccountUI(
    AdminListUserProfileController,
    AdminModifyUserController,
    AdminAssignProfileController,
    AdminViewUserController,
)


# Owner
OwnerAnalyticsVisitsYearController = AnalyticsVisitsYearController()
OwnerAnalyticsVisitsMonthController = AnalyticsVisitsMonthController()
OwnerAnalyticsVisitsWeekController = AnalyticsVisitsWeekController()
OwnerNumberOfVisits = NumberOfVisits(
    OwnerAnalyticsVisitsYearController,
    OwnerAnalyticsVisitsMonthController,
    OwnerAnalyticsVisitsWeekController,
)
OwnerAnalyticsDollarsSpentYearController = AnalyticsDollarsSpentYearController()
OwnerAnalyticsDollarsSpentMonthController = AnalyticsDollarsSpentMonthController()
OwnerAnalyticsDollarsSpentWeekController = AnalyticsDollarsSpentWeekController()
OwnerDollarsSpent = DollarsSpent(
    OwnerAnalyticsDollarsSpentYearController,
    OwnerAnalyticsDollarsSpentMonthController,
    OwnerAnalyticsDollarsSpentWeekController,
)
OwnerAnalyticsLengthBetweenCustomerVisitsController = (
    AnalyticsLengthBetweenCustomerVisitsController()
)
OwnerAvgLength = AvgLength(OwnerAnalyticsLengthBetweenCustomerVisitsController)
OwnerAnalyticsMenuItemsFrequencyTotalController = (
    AnalyticsMenuItemsFrequencyTotalController()
)
OwnerMenuItems = MenuItemsFrequency(OwnerAnalyticsMenuItemsFrequencyTotalController)

urlpatterns = [
    path("systime", sample.systime, name="systime"),
    path(
        "login",
        route(
            {
                "GET": loginUI.DisplayPage,
                "POST": loginUI.OnSubmit,
            },
        ),
        name="login",
    ),
    path("logout", logoutUI.DisplayPage, name="logoutUI"),
    path("logout/logout", logoutUI.Logout, name="logoutSubmit"),
    path(
        "admin/accounts/",
        route(
            {
                "GET": AdminSearchUsersUI.DisplayPage,
            }
        ),
        name="adminAccounts",
    ),
    path(
        "admin/accounts/modify/<username>",
        route(
            {
                "GET": AdminModifyUserUI.DisplayPage,
                "POST": AdminModifyUserUI.OnSubmit,
                "DELETE": AdminSuspendUserAccountUI.OnSubmit,
                "PUT": AdminUnsuspendUserAccountUI.OnSubmit,
            }
        ),
        name="adminModifyAccount",
    ),
    path(
        "admin/profiles/", AdminSearchUserProfilesUI.DisplayPage, name="adminProfiles"
    ),
    path(
        "admin/accounts/create",
        route(
            {
                "GET": AdminCreateUserAccountUI.DisplayPage,
                "POST": AdminCreateUserAccountUI.OnSubmit,
            }
        ),
        name="adminCreateAccount",
    ),
    path(
        "admin/profiles/create",
        route(
            {
                "GET": AdminCreateUserProfileUI.DisplayPage,
                "POST": AdminCreateUserProfileUI.OnSubmit,
            }
        ),
        name="adminCreateAccount",
    ),
    path(
        "admin/profiles/modify/<int:id>",
        route(
            {
                "GET": AdminModifyUserProfileUI.DisplayPage,
                "POST": AdminModifyUserProfileUI.OnSubmit,
                "DELETE": AdminDeleteUserProfileUI.OnSubmit,
            }
        ),
        name="adminModifyProfile",
    ),
    path("manager/menu/", ManagerViewMenuUI.DisplayPage, name="managerMenu"),
    path(
        "manager/menu/search/",
        ManagerSearchMenuItemUI.DisplayPage,
        name="managerMenuSearch",
    ),
    path(
        "manager/menu/<int:MenuItemID>/",
        route(
            {
                "GET": ManagerModifyMenuItemUI.DisplayPage,
                "POST": ManagerModifyMenuItemUI.OnSubmit,
                "DELETE": ManagerDeleteMenuItemUI.OnSubmit,
            }
        ),
        name="managerMenuItem",
    ),
    path(
        "manager/menu/create/",
        route(
            {
                "GET": ManagerCreateNewMenuItemUI.DisplayPage,
                "POST": ManagerCreateNewMenuItemUI.OnSubmit,
            }
        ),
        name="managerMenuItemCreate",
    ),
    path(
        "manager/category/",
        route(
            {
                "GET": ManagerViewCategoryUI.DisplayPage,
            }
        ),
        name="managerCategory",
    ),
    path(
        "manager/category/search/",
        ManagerSearchCategoryUI.DisplayPage,
        name="managerCategorySearch",
    ),
    path(
        "manager/category/add/",
        route(
            {
                "GET": ManagerAddCategoryUI.DisplayPage,
                "POST": ManagerAddCategoryUI.OnSubmit,
            }
        ),
        name="managerCategoryAdd",
    ),
    path(
        "manager/category/", ManagerViewCategoryUI.DisplayPage, name="managerCategory"
    ),
    path(
        "manager/category/search/",
        ManagerSearchCategoryUI.DisplayPage,
        name="managerCategorySearch",
    ),
    path(
        "manager/category/modify/<int:CID>",
        route(
            {
                "GET": ManagerModifyCategoryUI.DisplayPage,
                "PATCH": ManagerModifyCategoryUI.OnSubmit,
                "DELETE": ManagerDeleteCategoryUI.OnSubmit,
            }
        ),
        name="managerCategoryModify",
    ),
    path(
        "manager/couponCodes/",
        route(
            {
                "GET": ManagerViewCouponCodeUI.DisplayPage,
            }
        ),
        name="managerCouponCode",
    ),
    path(
        "manager/couponCodes/search/",
        ManagerSearchCouponCodeUI.DisplayPage,
        name="managerCouponCodesSearch",
    ),
    path(
        "manager/couponCodes/add/",
        route(
            {
                "GET": ManagerCreateCouponCodeUI.DisplayPage,
                "POST": ManagerCreateCouponCodeUI.OnSubmit,
            }
        ),
        name="managerCouponCodesCreate",
    ),
    path(
        "manager/couponCodes/modify/<int:CID>",
        route(
            {
                "GET": ManagerModifyCouponCodeUI.DisplayPage,
                "PATCH": ManagerModifyCouponCodeUI.OnSubmit,
                "DELETE": ManagerDeleteCouponCodeUI.OnSubmit,
            }
        ),
        name="managerCouponCodeModify",
    ),
    path(
        "tableno/",
        route(
            {
                "GET": GuestInputTableAndEmailUI.DisplayPage,
                "POST": GuestInputTableAndEmailUI.OnSubmit,
            }
        ),
        name="guestTableNo",
    ),
    path("", GuestBrowseMenuUI.DisplayPage, name="guestMenu"),
    path("search/", GuestBrowseMenuSearchUI.DisplayPage, name="guestMenuSearch"),
    path("<int:MenuItemID>/", GuestBrowseMenuItemUI.DisplayPage, name="guestMenuItem"),
    path(
        "cart/",
        route(
            {
                "PUT": GuestAddToCartUI.OnSubmit,
                "GET": GuestModifyCartUI.DisplayPage,
                "PATCH": GuestModifyCartUI.OnSubmit,
            }
        ),
        name="guestCart",
    ),
    path(
        "cart/submit/",
        route(
            {
                "GET": GuestSubmitCartUI.DisplayPage,
                "POST": GuestSubmitCartUI.OnSubmit,
            }
        ),
        name="guestCartSubmit",
    ),
    path(
        "cart/coupon/",
        route(
            {
                "POST": GuestSubmitCartUI.SetCouponCode,
                "DELETE": GuestSubmitCartUI.RemoveCouponCode,
            }
        ),
        name="guestCartCoupon",
    ),
    path("staff/orders/new", StaffViewMenuUI.DisplayPage, name="staffNewOrders"),
    path("staff/orders/ipo", StaffViewInProgress.DisplayPage, name="staffIPO"),
    path(
        "staff/orders/ready", StaffViewReadyOrders.DisplayPage, name="staffReadyOrders"
    ),
    path(
        "staff/orders/completed",
        StaffViewCompletedOrders.DisplayPage,
        name="staffCompletedOrders",
    ),
    path(
        "staff/orders/<int:orderID>/",
        route({"GET": StaffViewOrderDetailsUI.DisplayPage}),
        name="staffOrderDetails",
    ),
    path(
        "staff/order-item/",
        route({"POST": StaffUpdateOrderItem.Update}),
        name="staffOrderItem",
    ),
    path(
        "staff/order-itemQty/",
        route({"POST": StaffUpdateOrderQty.Update}),
        name="staffOrderItemQty",
    ),
    path(
        "owner/numberOfVisits/",
        OwnerNumberOfVisits.DisplayPage,
        name="ownerNumberOfVisits",
    ),
    path(
        "owner/dollarsSpent/",
        OwnerDollarsSpent.DisplayPage,
        name="ownerDollarsSpent",
    ),
    path(
        "owner/length/",
        OwnerAvgLength.DisplayPage,
        name="ownerLength",
    ),
    path(
        "owner/menu/",
        OwnerMenuItems.DisplayPage,
        name="ownerMenu",
    ),
]
