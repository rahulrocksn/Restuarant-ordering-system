import enum
from django.shortcuts import redirect, render, HttpResponse

from chewapp.common.auth_decorator import with_auth
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
from .templates import (
    getTabsOwner,
    getWeekMonthYearFromGet,
    getWeekRange,
    getYearRange,
    getMonthRange,
)
from ..common.error import Error
from django.utils.datastructures import MultiValueDictKeyError
from datetime import date


class NumberOfVisits:
    def __init__(
        self,
        analyticsVistsYear: AnalyticsVisitsYearController,
        analyticsVistsMonth: AnalyticsVisitsMonthController,
        analyticsVistsWeek: AnalyticsVisitsWeekController,
    ):
        self.analyticsVistsYear = analyticsVistsYear
        self.analyticsVistsMonth = analyticsVistsMonth
        self.analyticsVistsWeek = analyticsVistsWeek

    @with_auth(owner=True)
    def DisplayPage(self, request) -> render:

        try:

            # Check if there is data in GET
            week, month, year, GetDataMode = getWeekMonthYearFromGet(request)

            # Getting the number of weeks for selection query
            if GetDataMode == "Week" or GetDataMode == "Month":
                weeks = getWeekRange(year, month)
            else:
                weeks = None

            # Get data based on GetDataMode

            if GetDataMode == "Year":
                # Get the year data
                VisitsData, VisitsError = self.analyticsVistsYear.AnalyticsVisitsYear(
                    year
                )
            elif GetDataMode == "Month":
                # Get the month data
                StartDate = weeks[0].get("start_date")
                EndDate = weeks[-1].get("end_date")
                VisitsData, VisitsError = self.analyticsVistsMonth.AnalyticsVisitsMonth(
                    StartDate, EndDate
                )
            elif GetDataMode == "Week":
                # Get the week data
                week_start_zero = week - 1
                start = weeks[week_start_zero].get("start_date")
                VisitsData, VisitsError = self.analyticsVistsWeek.AnalyticsVisitsWeek(
                    start
                )

            if VisitsError is not None:
                return self.DisplayError(request, VisitsError)

            context = {
                "username": request.session.get("username", "error"),
                "profile": "owner",
                "tabs": getTabsOwner(request, "# visits"),
                "activeTab": "# visits",
                "GetDataMode": GetDataMode,
                "YearSelected": year,
                "Years": getYearRange(),
                "MonthSelected": month,
                "Months": getMonthRange(),
                "WeekSelected": week,
                "Weeks": weeks,
                "Data": VisitsData,
            }

            return render(request, "chewapp/OwnerNumberOfVisits.html", context)

        except Exception as ex:
            return self.DisplayError(request, Error(500, str(ex)))

    def DisplayError(self, request, error: Error):

        return HttpResponse(f"Error. Please refresh. {str(error)}", status=error.code)


class DollarsSpent:
    def __init__(
        self,
        analyticsDollarsSpentYear: AnalyticsDollarsSpentYearController,
        analyticsDollarsSpentMonth: AnalyticsDollarsSpentMonthController,
        analyticsDollarsSpentWeek: AnalyticsDollarsSpentWeekController,
    ):
        self.analyticsDollarsSpentYear = analyticsDollarsSpentYear
        self.analyticsDollarsSpentMonth = analyticsDollarsSpentMonth
        self.analyticsDollarsSpentWeek = analyticsDollarsSpentWeek

    @with_auth(owner=True)
    def DisplayPage(self, request) -> render:

        try:
            # Check if there is data in GET
            week, month, year, GetDataMode = getWeekMonthYearFromGet(request)

            # Getting the number of weeks for selection query
            if GetDataMode == "Week" or GetDataMode == "Month":
                weeks = getWeekRange(year, month)
            else:
                weeks = None

            # Get data based on GetDataMode

            if GetDataMode == "Year":
                # Get the year data
                (
                    SpentData,
                    SpentError,
                ) = self.analyticsDollarsSpentYear.AnalyticsDollarsSpentYear(year)
            elif GetDataMode == "Month":
                # Get the month data
                StartDate = weeks[0].get("start_date")
                EndDate = weeks[-1].get("end_date")
                (
                    SpentData,
                    SpentError,
                ) = self.analyticsDollarsSpentMonth.AnalyticsDollarsSpentMonth(
                    StartDate, EndDate
                )
            elif GetDataMode == "Week":
                # Get the week data
                week_start_zero = week - 1
                start = weeks[week_start_zero].get("start_date")
                (
                    SpentData,
                    SpentError,
                ) = self.analyticsDollarsSpentWeek.AnalyticsDollarsSpentWeek(start)

            if SpentError is not None:
                return self.DisplayError(request, SpentError)

            # Ensruing no "None" values in the data
            for i, item in enumerate(SpentData):
                if item is None:
                    SpentData[i] = 0

            context = {
                "username": request.session.get("username", "ERROR"),
                "profile": "owner",
                "tabs": getTabsOwner(request, "$ spent"),
                "activeTab": "$ spent",
                "GetDataMode": GetDataMode,
                "YearSelected": year,
                "Years": getYearRange(),
                "MonthSelected": month,
                "Months": getMonthRange(),
                "WeekSelected": week,
                "Weeks": weeks,
                "Data": SpentData,
            }

            return render(request, "chewapp/OwnerDollarsSpent.html", context)

        except Exception as ex:
            return self.DisplayError(request, Error(500, str(ex)))

    def DisplayError(self, request, error: Error):

        return HttpResponse(f"Error. Please refresh. {str(error)}", status=error.code)


class AvgLength:
    def __init__(self, controller: AnalyticsLengthBetweenCustomerVisitsController):
        self.controller = controller

    @with_auth(owner=True)
    def DisplayPage(self, request) -> render:

        try:
            SearchTerm = str(request.GET["SearchTerm"])
            if SearchTerm == "":
                SearchTerm = None
        except MultiValueDictKeyError:
            SearchTerm = None

        try:
            (
                AvgLengthData,
                AvgLengthError,
            ) = self.controller.AnalyticsLengthBetweenCustomerVisits()

            if AvgLengthError is not None:
                return self.DisplayError(request, AvgLengthError)

            AllUsers = [
                {"Email": email, "AvgFrequency": "{:.2f}".format(days)}
                for email, days in AvgLengthData.items()
            ]

            if len(AvgLengthData) != 0:
                AverageFrequency = "{:.2f}".format(
                    sum(AvgLengthData.values()) / len(AvgLengthData)
                )
            else:
                AverageFrequency = 0

            # Search
            if SearchTerm is not None:
                FilteredUsers = [
                    user
                    for user in AllUsers
                    if SearchTerm.lower() in user["Email"].lower()
                ]
            else:
                FilteredUsers = sorted(
                    AllUsers, key=lambda user: user["AvgFrequency"], reverse=True
                )

            context = {
                "username": request.session.get("username", "error"),
                "profile": "owner",
                "tabs": getTabsOwner(request, "Length between visits"),
                "activeTab": "Length between visits",
                "AverageFrequency": AverageFrequency,
                "Users": FilteredUsers,
                "SearchTerm": SearchTerm,
            }

            return render(request, "chewapp/OwnerAvgLength.html", context)

        except Exception as ex:
            return self.DisplayError(request, Error(500, str(ex)))

    def DisplayError(self, request, error: Error):

        return HttpResponse(f"Error. Please refresh. {str(error)}", status=error.code)


class MenuItemsFrequency:
    def __init__(
        self,
        analyticsMenuItemsFrequencyTotalController: AnalyticsMenuItemsFrequencyTotalController,
    ):

        self.analyticsMenuItemsFrequencyTotalController = (
            analyticsMenuItemsFrequencyTotalController
        )

    @with_auth(owner=True)
    def DisplayPage(self, request) -> render:

        try:
            SearchTerm = str(request.GET["SearchTerm"])
            if SearchTerm == "":
                SearchTerm = None
        except MultiValueDictKeyError:
            SearchTerm = None

        try:

            # Get data
            (
                FrequencyData,
                FrequencyError,
            ) = (
                self.analyticsMenuItemsFrequencyTotalController.AnalyticsMenuItemsFrequencyTotal()
            )

            if FrequencyError is not None:
                return self.DisplayError(request, FrequencyError)

            AllFoodItems = [
                {"Name": x.get("menu_item__name"), "Frequency": x.get("total")}
                for x in FrequencyData
            ]

            # Search
            if SearchTerm is not None:
                FilteredFoodItems = list()
                for item in AllFoodItems:
                    try:
                        if SearchTerm.lower() in item.get("Name").lower():
                            FilteredFoodItems.append(item)
                    except:
                        pass
            else:
                FilteredFoodItems = AllFoodItems

            context = {
                "username": request.session.get("username", "error"),
                "profile": "owner",
                "tabs": getTabsOwner(request, "Menu Items"),
                "activeTab": "Menu Items",
                "FoodItems": FilteredFoodItems,
                "SearchTerm": SearchTerm,
            }

            return render(request, "chewapp/OwnerMenuItems.html", context)

        except Exception as ex:
            return self.DisplayError(request, Error(500, str(ex)))

    def DisplayError(self, request, error: Error):

        return HttpResponse(f"Error. Please refresh. {str(error)}", status=error.code)
