import typing as tp
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия для управления HTTP-запросами с повторными попытками и тайм-аутами.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки между повторными попытками.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout

        # Настройка повторных попыток
        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        """
        Выполнить GET-запрос.

        :param url: URL для выполнения запроса.
        :param args: Дополнительные аргументы для запроса.
        :param kwargs: Дополнительные ключевые аргументы для запроса.
        :return: Объект Response от requests.
        """
        full_url = self.base_url + url
        return self.session.get(full_url, timeout=self.timeout, *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        """
        Выполнить POST-запрос.

        :param url: URL для выполнения запроса.
        :param args: Дополнительные аргументы для запроса.
        :param kwargs: Дополнительные ключевые аргументы для запроса.
        :return: Объект Response от requests.
        """
        full_url = self.base_url + url
        return self.session.post(full_url, timeout=self.timeout, *args, **kwargs)
