import requests
import time
import statistics
from typing import Optional, List, Dict
import dataclasses


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: List[Dict[str, any]]


class Session(requests.Session):
    def __init__(
            self,
            base_url: str,
            timeout: float = 5.0,
            max_retries: int = 3,
            backoff_factor: float = 0.3,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _request_with_retries(self, method, url, **kwargs):
        retries = 0
        while retries <= self.max_retries:
            try:
                response = super().request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                retries += 1
                if retries > self.max_retries:
                    raise e
                sleep_time = self.backoff_factor * (2 ** retries)
                time.sleep(sleep_time)

    def get(self, url, **kwargs) -> requests.Response:
        return self._request_with_retries("GET", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> requests.Response:
        return self._request_with_retries("POST", url, data=data, json=json, **kwargs)


def get_friends(user_id: int, fields: Optional[List[str]] = None) -> FriendsResponse:
    # В реальной программе нужно заменить VK_CONFIG данными конфигурации
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]

    fields_param = ",".join(fields) if fields else ""
    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields_param}&v={v}"

    session = Session(base_url=domain)
    response = session.get(query)
    data = response.json()

    friends = data['response']['items']
    count = data['response']['count']
    return FriendsResponse(count=count, items=friends)


def age_predict(user_id: int) -> Optional[float]:
    # Получаем друзей пользователя с полем bdate
    friends_data = get_friends(user_id, fields=['bdate'])

    # Список возрастов друзей
    ages = []

    current_year = time.localtime().tm_year

    for friend in friends_data.items:
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
