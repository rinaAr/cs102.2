import datetime as dt
import typing as tp
import statistics

from friends import get_friends


def calculate_age(bdate: str) -> tp.Optional[int]:
    """
    Вычислить возраст на основе строки даты рождения.

    :param bdate: Дата рождения в формате 'дд.мм.гггг'.
    :return: Возраст в годах или None, если формат некорректный.
    """
    try:
        birth_date = dt.datetime.strptime(bdate, "%d.%m.%Y").date()
        today = dt.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except (ValueError, TypeError):
        # Если дата рождения указана в неполном формате или некорректна
        return None


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    # Получаем список друзей с полем даты рождения (bdate)
    friends_data = get_friends(user_id, fields=['bdate'])

    # Список для хранения возрастов друзей
    ages = []

    for friend in friends_data.items:
        bdate = friend.get("bdate")
        if bdate:
            age = calculate_age(bdate)
            if age is not None:
                ages.append(age)

    if ages:
        # Возвращаем медиану возрастов
        return statistics.median(ages)

    # Если не удалось получить возраст ни одного друга
    return None
