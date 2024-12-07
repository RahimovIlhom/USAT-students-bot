from datetime import datetime

import pytz

TASHKENT_TIMEZONE = pytz.timezone('Asia/Tashkent')


async def get_tashkent_timezone(date: datetime = datetime.now()):
    if date is None:
        date = datetime.now()
    return date.replace(tzinfo=pytz.utc).astimezone(TASHKENT_TIMEZONE)
