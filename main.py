import traceback

from src.logger.logger import Logger
from src.processor.day_crawler import DayCrawler
from src.processor.process_checker import ProcessChecker
from src.reader.date_picker import DatePicker


def main():
    date_picker = DatePicker()
    date_picker.input_data()
    logger = Logger()
    for i, date in enumerate(date_picker.range()):
        if ProcessChecker.is_processed_earlier(date):
            logger.info(
                f'ignored {date} as it has already been crawled ({(i + 1) / len(date_picker) * 100:.1f}%, {i + 1}/{len(date_picker)})')
            continue
        logger.info(f'started {date}. ({(i + 1) / len(date_picker) * 100:.1f}%, {i + 1}/{len(date_picker)})')
        crawler = DayCrawler(date, logger)
        try:
            crawler.crawl()
        except Exception as e:
            logger.error(f'error occurred while crawling {date}.')
            logger.error(traceback.format_exc())
        else:
            ProcessChecker.check_as_processed(date)
            logger.info(f'finished {date}. crawled {len(crawler.items)} item(s).')


if __name__ == '__main__':
    main()
