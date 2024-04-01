from src.item import Item
from src.logger.logger import Logger
from src.processor.html_parser import DetailPageParser, ListPageParser
from src.reader.soup_request import SoupRequest
from src.writer.csv_writer import CSVWriter
from src.writer.image_writer import ImageWriter


class DayCrawler:
    def __init__(self, date: str, logger: Logger):
        self.date = date
        self._item_ids = []
        self.items = []
        self.csv_writer = CSVWriter(date)
        self.image_writer = ImageWriter()
        self.logger = logger

    def crawl(self):
        self._crawl_item_ids()
        self._crawl_item_data()
        for item in self.items:
            self.csv_writer.write(item)
            self.image_writer.write(item)

    def _crawl_item_ids(self):
        soup = SoupRequest.get_item_list_page_soup(self.date)
        last_page_number = DetailPageParser.get_last_page_number(soup)
        self.logger.info(f'  started collecting item ids. (page numbers={last_page_number})')

        for page_number in range(1, last_page_number + 1):
            self.logger.info(
                f'    collecting item ids. ({page_number / last_page_number * 100:.1f}%, {page_number}/{last_page_number})')
            soup = SoupRequest.get_item_list_page_soup(self.date, page_number)
            item_ids_of_the_page = ListPageParser.get_image_available_item_ids(soup)
            self._item_ids.extend(item_ids_of_the_page)

    def _crawl_item_data(self):
        self.logger.info(f'  started crawling item data. (target item numbers={len(self._item_ids)})')
        for i, item_id in enumerate(self._item_ids):
            self.logger.info(
                f'    crawling item. date={self.date}, id={item_id} ({(i + 1) / len(self._item_ids) * 100:.1f}%, {i + 1}/{len(self._item_ids)})')

            soup = SoupRequest.get_item_detail_page_soup(item_id)

            image_data = self._get_image_data(soup)
            if image_data['image'] is None:
                self.logger.debug(f'      item {item_id} has no image')
                continue

            text_data = self._get_text_data(soup)
            data = image_data | text_data
            self.items.append(Item(data))

    @staticmethod
    def _get_text_data(soup):
        upper_right_data = DetailPageParser.get_item_text_data_from_upper_right(soup)
        description_data = DetailPageParser.get_item_text_data_from_description(soup)
        result = description_data | upper_right_data
        return result

    @staticmethod
    def _get_image_data(soup):
        result = DetailPageParser.get_item_image_data(soup)
        return result
