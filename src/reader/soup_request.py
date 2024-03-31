import io
import time
from urllib.parse import urljoin

import requests
from PIL import Image
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class SoupRequest:
    def __init__(self):
        pass

    @staticmethod
    def get_item_list_page_soup(date: str, page_number: int = 1) -> BeautifulSoup:
        list_page_url = 'https://www.lost112.go.kr/find/findList.do'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': UserAgent().random}
        form_data = f'START_YMD={date}&END_YMD={date}&pageIndex={page_number}'
        for i in range(10):
            try:
                res = requests.post(list_page_url, headers=headers, data=form_data)
                res.raise_for_status()
                return BeautifulSoup(res.text, "lxml")
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                continue

    @staticmethod
    def get_item_detail_page_soup(item_id: str) -> BeautifulSoup:
        detail_page_url = 'https://www.lost112.go.kr/find/findDetail.do'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': UserAgent().random}
        form_data = f'ATC_ID={item_id}&FD_SN=1'
        for i in range(10):
            try:
                res = requests.post(detail_page_url, headers=headers, data=form_data)
                res.raise_for_status()
                return BeautifulSoup(res.text, "lxml")
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                continue

    @staticmethod
    def get_item_image(url: str) -> Image:
        base_url = 'https://www.lost112.go.kr/'
        full_url = urljoin(base_url, url)
        for i in range(10):
            try:
                res = requests.get(full_url, headers={'User-Agent': UserAgent().random})
                res.raise_for_status()
                image = Image.open(io.BytesIO(res.content))
                return image
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                continue
