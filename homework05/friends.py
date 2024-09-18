import requests
import dataclasses
import typing as tp
import time

# Для удобства типизации запросов
QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
        user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    """
    url = "https://api.vk.com/method/friends.get"
    params = {
        "user_id": user_id,
        "count": count,
        "offset": offset,
        "v": "5.131",
        "access_token": config.VK_ACCESS_TOKEN,  # Токен должен быть настроен
    }
    if fields:
        params["fields"] = ",".join(fields)

    response = requests.get(url, params=params).json()

    if "error" in response:
        raise Exception(f"Error fetching friends: {response['error']}")

    friends_data = response["response"]
    return FriendsResponse(count=friends_data["count"], items=friends_data["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
        source_uid: tp.Optional[int] = None,
        target_uid: tp.Optional[int] = None,
        target_uids: tp.Optional[tp.List[int]] = None,
        order: str = "",
        count: tp.Optional[int] = None,
        offset: int = 0,
        progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    """
    url = "https://api.vk.com/method/friends.getMutual"
    params = {
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": ",".join(map(str, target_uids)) if target_uids else None,
        "order": order,
        "count": count,
        "offset": offset,
        "v": "5.131",
        "access_token": config.VK_ACCESS_TOKEN,
    }

    # Удаляем None значения из параметров
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(url, params=params).json()

    if "error" in response:
        raise Exception(f"Error fetching mutual friends: {response['error']}")

    mutual_data = response["response"]

    # Если target_uids - возвращается список объектов с общими друзьями
    if isinstance(mutual_data, list) and isinstance(mutual_data[0], dict):
        mutual_friends = [
            MutualFriends(id=item["id"], common_friends=item["common_friends"], common_count=item["common_count"])
            for item in mutual_data
        ]
        return mutual_friends

    # Если это просто список ID
    return mutual_data


# Пример конфигурации
class config:
    VK_ACCESS_TOKEN = "ваш_токен"

