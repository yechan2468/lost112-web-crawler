from dataclasses import dataclass

from PIL import Image


@dataclass
class Item:
    id: str
    name: str
    category: str
    color: str
    date: str
    spotted_at: str
    registered_at: str
    now_kept_at: str
    status: str
    contact: str
    detail: str
    image_width: int
    image_height: int
    image_format: str
    image: Image

    def __init__(self, attributes):
        self.id = attributes["id"]
        self.name = attributes["name"]
        self.category = attributes["category"]
        self.color = attributes["color"]
        self.date = attributes["date"]
        self.spotted_at = attributes["spotted_at"]
        self.registered_at = attributes["registered_at"]
        self.now_kept_at = attributes["now_kept_at"]
        self.status = attributes["status"]
        self.contact = attributes["contact"]
        self.detail = attributes["detail"]
        self.image_width = attributes["image_width"]
        self.image_height = attributes["image_height"]
        self.image_format = attributes["image_format"]
        self.image = attributes["image"]
