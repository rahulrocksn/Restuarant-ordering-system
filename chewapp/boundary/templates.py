from calendar import monthrange
from datetime import date, timedelta
from typing import Tuple


from django.http import HttpRequest


def getTabs(request, selected):
    tabs = [
        {
            "title": "Menu Items",
            "link": request.build_absolute_uri("/manager/menu"),
            "selected": False,
        },
        {
            "title": "Coupons",
            "link": request.build_absolute_uri("/manager/couponCodes"),
            "selected": False,
        },
        {
            "title": "Categories",
            "link": request.build_absolute_uri("/manager/category"),
            "selected": False,
        },
    ]

    for tab in tabs:
        if tab["title"] == selected:
            tab["selected"] = True

    return tabs


def getStaffTabs(request, selected):
    tabs = [
        {
            "title": "New Orders",
            "link": request.build_absolute_uri("/staff/orders/new"),
            "selected": False,
        },
        {
            "title": "In Progress",
            "link": request.build_absolute_uri("/staff/orders/ipo"),
            "selected": False,
        },
        {
            "title": "Ready",
            "link": request.build_absolute_uri("/staff/orders/ready"),
            "selected": False,
        },
        {
            "title": "Completed",
            "link": request.build_absolute_uri("/staff/orders/completed"),
            "selected": False,
        },
    ]

    for tab in tabs:
        if tab["title"] == selected:
            tab["selected"] = True

    return tabs


def getTabsAdmin(request, selected):
    tabs = [
        {
            "title": "Users",
            "link": request.build_absolute_uri("/admin/accounts"),
            "selected": False,
        },
        {
            "title": "User Profiles",
            "link": request.build_absolute_uri("/admin/profiles"),
            "selected": False,
        },
    ]

    for tab in tabs:
        if tab["title"] == selected:
            tab["selected"] = True

    return tabs


def getTabsOwner(request, selected):
    tabs = [
        {
            "title": "# visits",
            "link": "/owner/numberOfVisits/",
            "selected": False,
        },
        {
            "title": "$ spent",
            "link": "/owner/dollarsSpent/",
            "selected": False,
        },
        {
            "title": "Length between visits",
            "link": "/owner/length/",
            "selected": False,
        },
        {
            "title": "Menu Items",
            "link": "/owner/menu/",
            "selected": False,
        },
    ]

    for tab in tabs:
        if tab["title"] == selected:
            tab["selected"] = True

    return tabs


def getYearRange():
    # Year ranges to be set in the dropdown

    # Start from this year:
    startYear = 2021

    # End at the current eyar:
    endYear = date.today().year

    # Create a list of years:
    return [year for year in range(startYear, endYear + 1)]


def getMonthRange():
    return [
        {"name": "Jan", "value": 1},
        {"name": "Feb", "value": 2},
        {"name": "Mar", "value": 3},
        {"name": "Apr", "value": 4},
        {"name": "May", "value": 5},
        {"name": "Jun", "value": 6},
        {"name": "Jul", "value": 7},
        {"name": "Aug", "value": 8},
        {"name": "Sep", "value": 9},
        {"name": "Oct", "value": 10},
        {"name": "Nov", "value": 11},
        {"name": "Dec", "value": 12},
    ]


def getWeekRange(year: int, month: int):
    # Gets date from sunday to sunday for each month.

    # unix date epoch for reference of number of days diff:
    epoch = date(1970, 1, 1)

    # Get the first day of the month:
    firstDay = date(year, month, 1)

    # Get the first day of the week:
    firstDayOfWeek = firstDay - timedelta(days=firstDay.weekday()) - timedelta(days=1)

    # Get the last day of the month:
    lastDay = date(year, month, monthrange(year, month)[1])

    # Get the last day of the week:
    if lastDay.weekday() == 6:
        lastDayOfWeek = lastDay + timedelta(days=7)
    else:
        lastDayOfWeek = (
            lastDay + timedelta(days=6 - lastDay.weekday()) - timedelta(days=1)
        )

    WeeksList = list()

    tempNo = 1
    tempDate = firstDayOfWeek

    while tempDate < lastDayOfWeek:
        WeeksList.append(
            {
                "week": tempNo,
                "start_date": tempDate,
                "end_date": tempDate + timedelta(days=6),
            }
        )
        tempDate += timedelta(days=7)
        tempNo += 1

    return WeeksList


def getSelectableProfiles():
    return [
        {"id": 1, "name": "Manager"},
        {"id": 2, "name": "Admin"},
        {"id": 3, "name": "Owner"},
        {"id": 4, "name": "Staff"},
    ]


def getWeekMonthYearFromGet(request: HttpRequest) -> Tuple[int, int, int, str]:
    # Check if there is week in GET
    try:
        week = int(request.GET["Week"])
        if week == 0 or week > 7:
            week = None
    except Exception:
        week = None

    # Check if there is month in GET
    try:
        month = int(request.GET["Month"])
        if month <= 0 or month > 12:
            month = None
    except Exception:
        month = None

    try:
        year = int(request.GET["Year"])
        if year < 2010 or year > date.today().year:
            year = None
    except Exception:
        # Set year as current year
        year = date.today().year

    mode = "Year"

    if year is not None:
        if month is not None:
            if week is not None:
                mode = "Week"
            else:
                mode = "Month"
        else:
            mode = "Year"

    return (week, month, year, mode)
