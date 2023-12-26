from datetime import datetime, timedelta
from typing import Iterable, List, Tuple


class PeriodTuple:
    def __init__(self, title: str, start_date: datetime, end_date: datetime):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date

    def to_list(self):
        return [self.title, self.start_date, self.end_date]

    def __str__(self):
        return self.title


class Period:
    DATE_FORMAT: str = "%d.%m.%Y"
    YESTERDAY = "YD"
    WEEK = "W"
    MONTH = "M"
    PREV_WEEK = "W0"
    PREV_MONTH = "M0"
    THIS_QUARTER = "Q"
    PREV_QUARTER = "Q0"
    THIS_YEAR = "Y"

    ALL_PERIODS: list = [
        YESTERDAY,
        WEEK,
        MONTH,
        PREV_WEEK,
        PREV_MONTH,
        THIS_QUARTER,
        PREV_QUARTER,
        THIS_YEAR,
    ]

    def __init__(self, period: str = YESTERDAY):
        yesterday = PeriodTuple(
            f"Вчера: {self._f(self._yesterday)}", *self.yesterday_period
        )
        past_week = PeriodTuple(
            "7 дней: с {0} по {1}".format(*self._f_list(p := self.past_days(7))), *p
        )
        past_month = PeriodTuple(
            "30 дней: с {0} по {1}".format(*self._f_list(p := self.past_days(30))), *p
        )
        previous_week = PeriodTuple(
            "Та неделя: {0} - {1}".format(
                *self._f_list(p := self.previous_week_period)
            ),
            *p,
        )
        previous_month = PeriodTuple(
            "Тот месяц: {0} - {1}".format(
                *self._f_list(p := self.previous_month_period)
            ),
            *p,
        )

        this_quarter = PeriodTuple(
            "Этот квартал: с {0} по {1}".format(
                *self._f_list(p := self.this_quarter_period)
            ),
            *p,
        )

        previous_quarter = PeriodTuple(
            "Тот квартал: с {0} по {1}".format(
                *self._f_list(p := self.previous_quarter_period)
            ),
            *p,
        )

        this_year = PeriodTuple(
            "Этот год: с {0} по {1}".format(*self._f_list(p := self.this_year_period)),
            *p,
        )

        self.period = period
        self.periods = {
            self.YESTERDAY: yesterday,
            self.WEEK: past_week,
            self.MONTH: past_month,
            self.PREV_WEEK: previous_week,
            self.PREV_MONTH: previous_month,
            self.THIS_QUARTER: this_quarter,
            self.PREV_QUARTER: previous_quarter,
            self.THIS_YEAR: this_year,
        }
        _tuple = self.periods.get(self.period)
        if not _tuple:
            raise AttributeError(
                f'Period "{period}" not exists. choose in {self.periods.keys()}',
            )
        self.title, self.start_date, self.end_date = _tuple.to_list()

    @property
    def today(self) -> datetime:
        return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    @property
    def _yesterday(self) -> datetime:
        return self.today - timedelta(days=1)

    @property
    def previous_week_period(self) -> Tuple[datetime, datetime]:
        last_week = self.today - timedelta(days=7)
        start_date = last_week - timedelta(days=last_week.weekday())
        end_date = start_date + timedelta(days=6)
        return start_date, self._to_last_second(end_date)

    @property
    def previous_month_period(self) -> Tuple[datetime, datetime]:
        end_date = self.today.replace(day=1) - timedelta(days=1)
        start_date = end_date.replace(day=1)
        return start_date, self._to_last_second(end_date)

    @property
    def yesterday_period(self) -> Tuple[datetime, datetime]:
        return self._yesterday, self._to_last_second(self._yesterday)

    @property
    def this_quarter_period(self) -> Tuple[datetime, datetime]:
        this_quarter = self._get_quarter(self.today)
        return self.get_periods_from_quarter(quarter=this_quarter, year=self.today.year)

    @property
    def previous_quarter_period(self) -> Tuple[datetime, datetime]:
        this_quarter = self._get_quarter(self.today)
        quarter = this_quarter - 1 if this_quarter != 1 else 4
        year = self.today.year if this_quarter != 1 else self.today.year - 1
        return self.get_periods_from_quarter(quarter=quarter, year=year)

    @property
    def this_year_period(self) -> Tuple[datetime, datetime]:
        end_date = self._to_last_second(self._yesterday)
        start_date = end_date.replace(month=1, day=1)
        return start_date, self._to_last_second(end_date)

    def past_days(self, days: int) -> Tuple[datetime, datetime]:
        end_date = self._to_last_second(self._yesterday)
        start_date = (end_date - timedelta(days=days)) + timedelta(seconds=1)
        return start_date, end_date

    @property
    def days_since(self) -> int:
        return (self.end_date - self.start_date).days + 1

    @staticmethod
    def _get_quarter(dt: datetime) -> int:
        return (dt.month - 1) // 3 + 1

    @staticmethod
    def get_periods_from_quarter(
        quarter: int,
        year: int,
    ) -> Tuple[datetime, datetime]:
        if quarter in [1, "1"]:
            return datetime(year=year, month=1, day=1), datetime(
                year=year,
                month=3,
                day=31,
            )
        if quarter in [2, "2"]:
            return datetime(year=year, month=4, day=1), datetime(
                year=year,
                month=6,
                day=30,
            )
        if quarter in [3, "3"]:
            return datetime(year=year, month=7, day=1), datetime(
                year=year,
                month=9,
                day=30,
            )
        if quarter in [4, "4"]:
            return datetime(year=year, month=10, day=1), datetime(
                year=year,
                month=12,
                day=31,
            )
        else:
            raise ValueError(f"Quarter: '{quarter}' is not valid quarter")

    @staticmethod
    def _to_last_second(dt: datetime) -> datetime:
        return dt.replace(hour=23, minute=59, second=59)

    @staticmethod
    def _f(d: datetime, date_format: str = DATE_FORMAT) -> str:
        return d.strftime(date_format)

    def _f_list(self, dates: Iterable) -> List[str]:
        formatted_dates = []
        for dt in dates:
            formatted_dates.append(self._f(dt))
        return formatted_dates
