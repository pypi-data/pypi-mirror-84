# from contextlib import AbstractContextManager

import logging

import httpx

from .constants import API_BASE_URL, ERROR_DICT

logger = logging.getLogger(__name__)


def parse_error_code(error_code):
    return ERROR_DICT.get(error_code, "unknown error")


class BaseHTTPAdapter:
    client = None

    def get(self, url):
        raise NotImplementedError

    def get_with_data(self, url, data):
        raise NotImplementedError

    def post(self, url, data):
        raise NotImplementedError


class AsyncHTTPAdapter(BaseHTTPAdapter):
    pass


class SyncHTTPAdapter(BaseHTTPAdapter):
    client = httpx.Client(base_url=API_BASE_URL)

    def get_with_data(self, url, data):
        logger.debug(f"[SyncHTTPAdapter:get_with_data] URL: {url}")
        with self.client as client:
            response = client.request(method="GET", url=url, json=data)
            return response.json()

    def get(self, url):
        logger.debug(f"[SyncHTTPAdapter:get] URL: {url}")

        with self.client as client:
            response = client.get(url)
            return response.json()

    def post(self, url, data):
        logger.debug(f"[SyncHTTPAdapter:post] URL: {url}")

        with self.client as client:
            response = client.post(url, json=data)
            return response.json()


def get_http_adapter():
    # TODO: If async is supported, use the AsyncHTTPAdapter
    return SyncHTTPAdapter()
