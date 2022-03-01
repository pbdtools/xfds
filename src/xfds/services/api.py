"""Base Classes for Interacting with services."""
import requests


class BaseAPI:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_page(self, url: str, params: dict = None) -> dict:
        """Get page data."""
        response = requests.get(url, params=params)
        return response.json()

    def get(self, endpoint: str, params: dict = None) -> list[dict]:
        """GET request.

        Iterate through pages based on logic from BaseAPI._get_next.
        """
        url = self.base_url + endpoint
        data: list[dict] = []
        while url:
            page_data = self.get_page(url, params=params)
            data.extend(self._data_from_page(page_data))
            url = self._get_next(page_data)
        return data

    def _get_next(self, data: dict) -> str:
        """Get next page.

        Assumes that the API response has a `next` key indicating the next page.
        If not, this returns a blank url string to exit the loop.
        """
        try:
            return data.get("next", "")
        except AttributeError:
            return ""

    def _data_from_page(self, data: dict) -> dict:
        """Extact data from page.

        Assumes that the whole response is a list of data.
        """
        return data
