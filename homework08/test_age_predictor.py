import statistics

import pytest
from age_predictor import Session, get_friends, extract_age, age_predict
from datetime import datetime

# Мок данных друзей
class MockSession:
    def __init__(self):
        self.base_url = "https://mockapi.com"
        self.timeout = 5.0
        self.max_retries = 3
        self.backoff_factor = 0.3
        self.access_token = "mock_access_token"
        self.version = "5.131"

    def get(self, url, params=None):
        return MockResponse()

    def post(self, url, data=None, json=None, **kwargs):
        return MockResponse()

class MockResponse:
    def json(self):
        return {
            "response": {
                "count": 3,
                "items": [
                    {"bdate": "25.12.1995"},
                    {"bdate": "15.06.1989"},
                    {"bdate": "03.03.2000"},
                ]
            }
        }

def test_extract_age():
    assert extract_age("25.12.1995") == datetime.now().year - 1995
    assert extract_age("12.04") is None
    assert extract_age("01.01.2000") == datetime.now().year - 2000
    assert extract_age("") is None

def test_age_predict():
    session = MockSession()
    assert age_predict(session, 123456) == statistics.median([
        datetime.now().year - 1995,
        datetime.now().year - 1989,
        datetime.now().year - 2000
    ])
