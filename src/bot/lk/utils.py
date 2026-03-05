import datetime

from pytils import numeral

from src.bot.lk.dto import TimeDTO, HumanizeTimeDTO


def get_time_until_expiration(date_of_expiration: datetime.datetime) -> TimeDTO:
    remaining_time = date_of_expiration - datetime.datetime.now()
    days = divmod(remaining_time.total_seconds(), 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    return TimeDTO(
        days=days[0],
        hours=hours[0],
        minutes=minutes[0],
        seconds=seconds[0],
    )


def humanize_time(time_dto: TimeDTO) -> HumanizeTimeDTO:
    days = numeral.get_plural(time_dto.days, "день, дня, дней")
    hours = numeral.get_plural(time_dto.hours, "час, часа, часов")
    minutes = numeral.get_plural(time_dto.minutes, "минута, минуты, минут")
    seconds = numeral.get_plural(time_dto.seconds, "секунда, секунды, секунд")
    return HumanizeTimeDTO(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )
