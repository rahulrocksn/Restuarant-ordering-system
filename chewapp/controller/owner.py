import enum
from typing import List, Tuple, Mapping, Any
from ..common.error import Result, Error
from ..models import Order, OrderItem, OrderStatus, MenuItem
from datetime import datetime, timedelta, timezone
from django.db.models import Sum, Count
import functools


def datetimetz(*args):
    return datetime(*args, tzinfo=timezone.utc)


def make_dates(
    *,
    date_start: datetime,
    date_end: datetime,
    n_buckets: int = None,
    bucket_size: timedelta = None,
) -> Tuple[List[datetime], timedelta]:
    duration = date_end - date_start

    if bucket_size is None and n_buckets is not None:
        bucket_size = duration / n_buckets
    if bucket_size is not None and n_buckets is None:
        n_buckets = int(duration / bucket_size)

    if n_buckets is None or bucket_size is None:
        return [], timedelta(0)

    return (
        [date_start + (i * bucket_size) for i in range(n_buckets)],
        bucket_size,
    )


def aggregate(
    *,
    date_start: datetime,
    date_end: datetime,
    n_buckets: int = None,
    bucket_size: timedelta = None,
    filters={},
    fn=lambda bucket_start, bucket_size: Order.objects.filter(
        created_at__gte=bucket_start,
        created_at__lt=bucket_start + bucket_size,
    ).count(),
) -> Result[List[Any]]:
    try:
        dates, bucket_size = make_dates(
            date_start=date_start,
            date_end=date_end,
            n_buckets=n_buckets,
            bucket_size=bucket_size,
        )

        return [fn(bucket_start, bucket_size) for bucket_start in dates], None
    except Exception as ex:
        return None, Error(500, str(ex))


def make_params(agg_type, date_start: datetime, date_end: datetime = None):
    if agg_type == "year":
        return {
            "date_start": datetimetz(date_start.year, 1, 1),
            "date_end": datetimetz(date_start.year + 1, 1, 1),
            "n_buckets": 12,
        }
    elif agg_type == "month":
        return {
            "date_start": datetimetz(date_start.year, date_start.month, date_start.day),
            "date_end": datetimetz(date_end.year, date_end.month + 1, date_end.day),
            "bucket_size": timedelta(days=7),
        }
    elif agg_type == "week":
        return {
            "date_start": date_start,
            "date_end": date_start + timedelta(days=7),
            "n_buckets": 7,
        }

    raise Exception("Invalid agg_type: " + agg_type)


class AnalyticsVisitsYearController:
    def AnalyticsVisitsYear(self, year) -> Result[List[float]]:
        return aggregate(**make_params("year", datetime(year, 1, 1)))


class AnalyticsVisitsMonthController:
    def AnalyticsVisitsMonth(self, date_start, date_end) -> Result[List[float]]:
        return aggregate(**make_params("month", date_start, date_end))


class AnalyticsVisitsWeekController:
    def AnalyticsVisitsWeek(self, date_start) -> Result[List[float]]:
        return aggregate(**make_params("week", date_start))


def aggfn_dollars_spent(bucket_start, bucket_size):
    return Order.objects.filter(
        created_at__gte=bucket_start,
        created_at__lt=bucket_start + bucket_size,
    ).aggregate(Sum("total_price"))["total_price__sum"]


class AnalyticsDollarsSpentYearController:
    def AnalyticsDollarsSpentYear(self, year) -> Result[List[float]]:
        return aggregate(
            **make_params("year", datetime(year, 1, 1)),
            fn=aggfn_dollars_spent,
        )


class AnalyticsDollarsSpentMonthController:
    def AnalyticsDollarsSpentMonth(self, date_start, date_end) -> Result[List[float]]:

        month = list()

        while date_start < date_end:
            month.append(
                aggregate(
                    **make_params("week", date_start),
                    fn=aggfn_dollars_spent,
                )[0]
            )
            date_start += timedelta(days=7)

        NewMonth = list()

        for week in month:
            sum = 0
            for day in week:
                if day is not None:
                    sum += day
            NewMonth.append(sum)

        return (NewMonth, None)


class AnalyticsDollarsSpentWeekController:
    def AnalyticsDollarsSpentWeek(self, date_start) -> Result[List[float]]:
        return aggregate(
            **make_params("week", date_start),
            fn=aggfn_dollars_spent,
        )


def aggfn_menuitem_frequency(bucket_start, bucket_size):
    return functools.reduce(
        lambda acc, v: {**acc, v["menu_item__name"]: v["total"]},
        OrderItem.objects.filter(
            order__created_at__gte=bucket_start,
            order__created_at__lt=bucket_start + bucket_size,
        )
        .values("menu_item__name")
        .annotate(total=Count("id"))
        .all(),
        {},
    )


class AnalyticsMenuItemsFrequencyTotalController:
    def AnalyticsMenuItemsFrequencyTotal(self) -> Result[List[Mapping]]:
        try:
            return (
                OrderItem.objects.values("menu_item__name")
                .annotate(total=Count("id"))
                .all(),
                None,
            )
        except Exception as ex:
            return (None, Error(500, str(ex)))


class AnalyticsLengthBetweenCustomerVisitsController:
    def AnalyticsLengthBetweenCustomerVisits(self) -> Result[dict]:
        try:

            # This code sucks, but IDK how to implement it right now. So expect it to be slow and not scale...

            # This is the most naive way to do this. <- this comment was from co-pilot

            emailList = [
                email[0]
                for email in Order.objects.order_by().values_list("email").distinct()
            ]

            AccountDict = dict()

            for email in emailList:
                daysBetween = list()
                orders = Order.objects.filter(email=email).order_by("created_at")

                for i in range(len(orders) - 1):
                    if i + 1 < len(orders):
                        daysBetween.append(
                            (orders[i + 1].created_at - orders[i].created_at).days
                        )

                if len(daysBetween) > 0:
                    AccountDict[email] = sum(daysBetween) / len(daysBetween)
                else:
                    AccountDict[email] = 0

            return (AccountDict, None)
        except Exception as ex:
            return (None, Error(500, str(ex)))
