import pytest
import statistics
from typing import Optional


# Мок данных друзей
mock_friends_response = {
    'response': {
        'count': 3,
        'items': [
            {'id': 1, 'bdate': '15.6.1990'},
            {'id': 2, 'bdate': '3.9.1985'},
            {'id': 3, 'bdate': '12.2.2000'},
        ]
    }
}

mock_friends_response_no_year = {
    'response': {
        'count': 2,
        'items': [
            {'id': 1, 'bdate': '15.6'},  # Без года
            {'id': 2, 'bdate': '3.9'},   # Без года
        ]
    }
}

mock_friends_response_partial_year = {
    'response': {
        'count': 3,
        'items': [
            {'id': 1, 'bdate': '15.6'},  # Без года
            {'id': 2, 'bdate': '3.9.1985'},
            {'id': 3, 'bdate': '12.2.2000'},
        ]
    }
}


# Мок функций для получения друзей
def mock_get_friends_response(user_id: int, fields: Optional[list] = None):
    return mock_friends_response

def mock_get_friends_response_no_year(user_id: int, fields: Optional[list] = None):
    return mock_friends_response_no_year

def mock_get_friends_response_partial_year(user_id: int, fields: Optional[list] = None):
    return mock_friends_response_partial_year


# Функция age_predict (модифицированная для тестов)
def age_predict(user_id: int, get_friends_func) -> Optional[float]:
    # Получаем друзей пользователя с полем bdate
    friends_data = get_friends_func(user_id, fields=['bdate'])

    # Список возрастов друзей
    ages = []

    current_year = 2024  # Для тестов установим фиксированный год

    for friend in friends_data['response']['items']:
        try:
            bdate = friend.get('bdate', None)
            if bdate and len(bdate.split('.')) == 3:  # Проверяем, что дата содержит день, месяц и год
                day, month, year = map(int, bdate.split('.'))
                age = current_year - year
                ages.append(age)
        except Exception:
            pass  # Игнорируем друзей с некорректными данными

    # Если список возрастов пуст, возвращаем None
    if not ages:
        return None

    # Возвращаем медианный возраст
    return statistics.median(ages)


# Тесты
def test_age_predict_with_valid_friends():
    # Используем функцию, возвращающую мок данных друзей
    predicted_age = age_predict(1234567, mock_get_friends_response)
    assert predicted_age == 34, f"Expected 34, got {predicted_age}"


def test_age_predict_with_no_year_in_bdate():
    # Используем функцию, где нет года рождения
    predicted_age = age_predict(1234567, mock_get_friends_response_no_year)
    assert predicted_age is None, f"Expected None, got {predicted_age}"


def test_age_predict_with_partial_year_in_bdate():
    # Используем функцию, где только часть друзей указала год рождения
    predicted_age = age_predict(1234567, mock_get_friends_response_partial_year)
    assert predicted_age == 31.5, f"Expected 31.5, got {predicted_age}"



# Запуск тестов
if __name__ == "__main__":
    pytest.main()
