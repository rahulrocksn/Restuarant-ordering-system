from typing import List
from ..common.error import Result, Error
from ..models import MenuItem, Category, CouponCode
from django.db import transaction


class ViewMenuController:
    def __init__(self):
        pass

    def GetMenuItems(self) -> Result[List[MenuItem]]:
        return MenuItem.GetAll(), None

    def ViewMI(self, MIID) -> Result[MenuItem]:
        try:
            m = MenuItem.objects.get(id=MIID)
            return m, None
        except Exception as ex:
            return None, Error(500, "Failed to view:" + str(ex))


class CreateNewMenuItemController:
    def __init__(self):
        pass

    def CreateNewMI(self, Name, Desc, Price, Stock, File=None) -> Result[MenuItem]:

        try:
            with transaction.atomic():

                m = MenuItem(
                    name=Name,
                    description=Desc,
                    price=Price,
                    stock=Stock,
                )
                if File is not None:
                    m.menuImg.save(File.name, File.file)
                m.save()
            return m, None
        except Exception as ex:
            return None, Error(500, "Failed to create:" + str(ex))


class DeleteMenuItemController:
    def __init__(self):
        pass

    def DeleteMI(self, MIID):
        try:
            d = MenuItem.objects.get(id=MIID)
            d.delete()
            return True, None
        except Exception as ex:
            return False, Error(500, "Failed to delete:" + str(ex))


class SearchMenuItemController:
    def __init__(self):
        pass

    def SearchMI(self, NameMI) -> Result[List[MenuItem]]:
        try:
            return MenuItem.objects.filter(name__icontains=NameMI), None
        except Exception as ex:
            return None, Error(500, "Failed to search:" + str(ex))


class ModifyMenuItemController:
    def __init__(self):
        pass

    def ModifyMI(self, MIID, Name, Desc, Price, Stock, File) -> Result[MenuItem]:
        try:
            m = MenuItem.objects.get(id=MIID)
            m.name = Name
            m.description = Desc
            m.price = Price
            m.stock = Stock

            if File is not None:
                m.menuImg.save(File.name, File.file),

            m.save()
            return m, None

        except Exception as ex:
            return None, Error(500, "Failed to modify:" + str(ex))


class CreateCouponCodeController:
    def __init__(self):
        pass

    # use the same for create and modify
    def CreateCouponCode(self, Code, Percent, Dollar, MinSpend) -> Result[CouponCode]:
        try:
            if CouponCode.objects.filter(code=Code).exists():
                c = CouponCode.objects.get(code=Code)
                c.code = Code
                c.discount_percent = Percent
                c.discount_dollar = Dollar
                c.min_spend = MinSpend
                c.save()

                return c, None

            else:
                coupon = CouponCode(
                    code=Code,
                    discount_percent=Percent,
                    discount_dollar=Dollar,
                    min_spend=MinSpend,
                )
                coupon.save()
                return coupon, None

        except Exception as ex:
            return None, Error(500, "Failed to create:" + str(ex))


class DeleteCouponCodeController:
    def __init__(self):
        pass

    def DeleteCouponCode(self, CID) -> Result[List[CouponCode]]:
        try:
            d = CouponCode.objects.filter(id=CID)
            d.delete()

            return True, None
        except Exception as ex:
            return False, Error(500, "Failed to delete:" + str(ex))


class SearchCouponCodeController:
    def __init__(self):
        pass

    def SearchCouponCode(self, Code) -> Result[List[CouponCode]]:
        try:
            return CouponCode.SearchKey(Code), None
        except Exception as ex:
            return None, Error(500, "Failed to search:" + str(ex))


class ViewCouponCodeController:
    def __init__(self):
        pass

    def ViewCouponCode(self, CID) -> Result[CouponCode]:
        try:
            c = CouponCode.objects.get(id=CID)
            return c, None
        except Exception as ex:
            return None, Error(500, "Failed to view coupon code:" + str(ex))


# add diagrams for this if this is needed
class GetAllCouponCodeController:
    def __init__(self):
        pass

    def GetAllCouponCodes(self) -> Result[List[CouponCode]]:
        try:
            return CouponCode.GetAll(), None
        except Exception as ex:
            return None, Error(500, "Failed to get coupon code:" + str(ex))


class ViewCategoryController:
    def __init__(self):
        pass

    def ViewCategory(self) -> Result[List[Category]]:
        try:
            return Category.GetAll(), None
        except Exception as ex:
            return None, Error(500, "Failed to get coupon code:" + str(ex))

    def GetCategory(self, CatID) -> Result[Category]:
        try:
            return Category.objects.get(id=CatID), None
        except Exception as ex:
            return None, Error(500, "Failed to get:" + str(ex))

    def GetCategoryMenuItems(self, CatID) -> Result[List[MenuItem]]:
        try:
            return MenuItem.objects.filter(categories__id=CatID), None
        except Exception as ex:
            return None, Error(500, "Failed to get:" + str(ex))


class AddCategoryController:
    def __init__(self):
        pass

    def GetCategories(self) -> Result[List[Category]]:
        return Category.GetAll(), None

    def AddCategory(self, CatName, Desc, MIIDs) -> Result[Category]:
        try:
            with transaction.atomic():
                cat = Category(name=CatName, description=Desc)
                cat.save()

                for ID in MIIDs:
                    menu = MenuItem.objects.get(id=ID)
                    cat.menuItem.add(menu)

                return cat, None

        except Exception as ex:
            return None, Error(500, "Failed to create:" + str(ex))


class ModifyCategoryController:
    def __init__(self):
        pass

    def ModifyCategory(self, CID, Name, Desc, MIIDs) -> Result[Category]:
        try:
            cat = Category.objects.filter(id=CID)
            cat.update(name=Name, description=Desc)

            c = Category.objects.get(id=CID)

            for id in MIIDs:
                menu = MenuItem.objects.filter(id=id)
                # This block filters the menu items that were added before but are unselected the next time they are modified
                check = c.menuItem.through.objects.filter(category_id=c.id).exclude(
                    menuitem_id__in=MIIDs
                )
                c.menuItem.add(*menu)
                # Here it deletes the ones whicih are excluded from the list
                check.delete()

            return cat, None

        except Exception as ex:
            return None, Error(500, "Failed to modify:" + str(ex))


class DeleteCategoryController:
    def __init__(self):
        pass

    def DeleteCategory(self, CategoryID):
        try:
            d = Category.objects.get(id=CategoryID)
            d.delete()
            return True, None
        except Exception as ex:
            return False, Error(500, "Failed to delete:" + str(ex))


class SearchCategoryController:
    def __init__(self):
        pass

    def SearchCategory(self, CatName) -> Result[List[Category]]:
        try:
            return Category.SearchKey(CatName), None
        except Exception as ex:
            return None, Error(500, "Failed to search:" + str(ex))
