import time
import requests
import typing as tp
import statistics
from datetime import datetime
from requests.exceptions import RequestException
import dataclasses


class Session(requests.Session):
    def __init__(
            self,
            base_url: str,
            timeout: float = 5.0,
            max_retries: int = 3,
            backoff_factor: float = 0.3,
            access_token: str = "",
            version: str = "5.131"
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.access_token = access_token
        self.version = version

    def _retry(self, func: tp.Callable, url: str, **kwargs: tp.Any) -> requests.Response:
        retries = 0
        while retries < self.max_retries:
            try:
                response = func(f"{self.base_url}/{url}", timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except (RequestException, requests.exceptions.HTTPError) as e:
                retries += 1
                wait_time = self.backoff_factor * (2 ** retries)
                time.sleep(wait_time)
        raise requests.exceptions.RetryError(f"Max retries exceeded for URL: {url}")

    def get(self, url, **kwargs: tp.Any) -> requests.Response:
        return self._retry(super().get, url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs: tp.Any) -> requests.Response:
        return self._retry(super().post, url, data=data, json=json, **kwargs)


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.List[tp.Dict[str, tp.Any]]


def get_friends(
        session: Session, user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    params = {
        "access_token": session.access_token,
        "user_id": user_id,
        "count": count,
        "offset": offset,
        "v": session.version,
    }
    if fields:
        params["fields"] = ",".join(fields)

    response = session.get("friends.get", params=params)
    data = response.json()["response"]

    return FriendsResponse(count=data["count"], items=data["items"])


def extract_age(bdate: str) -> tp.Optional[int]:
    try:
        day, month, year = map(int, bdate.split('.'))
        return datetime.now().year - year
    except ValueError:
        return None


def age_predict(session: Session, user_id: int) -> tp.Optional[float]:
    friends = get_friends(session, user_id, fields=["bdate"])

    ages = []
    for friend in friends.items:
        bdate = friend.get("bdate")
        if bdate:
            age = extract_age(bdate)
            if age:
                ages.append(age)

    if not ages:
        return None

    return statistics.median(ages)
