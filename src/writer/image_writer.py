import os

from src.item import Item


class ImageWriter:
    def __init__(self):
        pass

    @staticmethod
    def write(item: Item):
        year, month, date = item.date[:4], item.date[4:6], item.date[6:]
        filepath = f'output/image/{year}/{month}/{date}/{item.id}.{item.image_format}'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        item.image.save(filepath)
