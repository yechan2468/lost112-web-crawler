import csv
import os

from src.item import Item


class CSVWriter:
    def __init__(self, date: str):
        filepath = f'output/csv/{date[:6]}.csv'
        os.makedirs(os.path.dirname('output/csv'), exist_ok=True)
        f = open(filepath, 'a', newline='', encoding='utf-8')
        self._writer = csv.writer(f)

    def write(self, item: Item):
        self._writer.writerow([
            item.id,
            item.name,
            item.category,
            item.color,
            item.date,
            item.spotted_at,
            item.registered_at,
            item.now_kept_at,
            item.status,
            item.detail,
            item.image_width,
            item.image_height,
            item.image_format
        ])
