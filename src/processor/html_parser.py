import re

from bs4 import BeautifulSoup

from src.reader.soup_request import SoupRequest


class ListPageParser:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_image_available_item_ids(soup):
        result = []
        rows = soup.select('#contents > div.find_listBox > table > tbody > tr')
        for row in rows:
            if ListPageParser._is_item_has_image(row):
                item_id = row.select_one('td:nth-child(1) > a').text.strip()
                result.append(item_id)
        return result

    @staticmethod
    def _is_item_has_image(table_row: BeautifulSoup):
        return table_row.select_one('td:nth-child(2) > div.title_text > a > img') is not None


class DetailPageParser:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_item_text_data_from_upper_right(soup: BeautifulSoup):
        result = {}

        korean_key_to_english_key = {
            '관리번호': 'id',
            '습득일': 'date',
            '습득장소': 'spotted_at',
            '물품분류': 'category',
            '접수장소': 'registered_at',
            '보관장소': 'now_kept_at',
            '유실물상태': 'status',
            '보관장소연락처': 'contact'
        }

        item_name = soup.select_one('#contents > div.findDetail > div.findDetail_wrap > div.find_info > p') \
            .text.split(':')[1].strip()
        result['name'] = item_name

        upper_right_elems = soup.select('#contents > div.findDetail > div.findDetail_wrap > div.find_info > ul > li')
        for elem in upper_right_elems:
            key = elem.select_one('p.find01').text
            value = elem.select_one('p.find02').text.strip()
            if key == '관리번호':  # F2024032900002344-1
                value = value.rstrip('-1')
            elif key == '습득일':  # 2024-03-01 12시경
                value = value[:10].replace('-', '')
            elif key == '물품분류':  # 카드 &gt; 신용(체크)카드
                value = value.replace('&gt;', '>')
            else:
                pass
            result[korean_key_to_english_key[key]] = value

        return result

    @staticmethod
    def get_item_text_data_from_description(soup: BeautifulSoup):
        result = {'name': None, 'color': None, 'detail': None}
        korean_key_to_english_key = {
            '물품명': 'name',
            '물품색상': 'color',
            '특이사항': 'detail',
        }
        description_lines = list(map(str, soup.select_one('#contents > div.findDetail > div.find_info_txt').contents))

        for line in description_lines:
            if '습득/보관' in line:  # 서울서초경찰서에서는 [2023.01.02] [에어팟2세대 한쪽유닛(화이트(흰)색)]을 습득/보관 하였습니다.
                name_and_color = re.findall(r'\[.*\].*\[(.*)\]', line)[0]  # 에어팟2세대 한쪽유닛(화이트(흰)색)
                seperator = DetailPageParser._get_name_and_color_seperator_index(name_and_color)
                result[korean_key_to_english_key['물품명']] = name_and_color[:seperator].strip()
                result[korean_key_to_english_key['물품색상']] = name_and_color[seperator:].strip(' ()')
            elif '특이' in line:  # 특이사항 : 없음\r\n\t\t\t
                splitted = line.rstrip().split(':')  # 없음
                result[korean_key_to_english_key['특이사항']] = splitted[1].strip() if len(splitted) > 1 else '없음'

        return result

    @staticmethod
    def _get_name_and_color_seperator_index(name_and_color: str):
        index = len(name_and_color)
        stack_size = 0
        for char in reversed(name_and_color):
            index -= 1
            if char == ')':
                stack_size += 1
            elif char == '(':
                stack_size -= 1
                if stack_size == 0:
                    break
        return index

    @staticmethod
    def get_item_image_data(soup: BeautifulSoup):
        result = {'image': None, 'image_width': 0, 'image_height': 0, 'image_format': ''}
        image_url = soup.select_one(
            '#contents > div.findDetail > div.findDetail_wrap > div.img_area > p.lost_img > img').attrs['src']
        if image_url == '/lostnfs/images/sub/img04_no_img.gif':
            return result

        result['image_format'] = image_url.split('.')[-1]
        item_image = SoupRequest.get_item_image(image_url)
        result['image'] = item_image
        result['image_width'], result['image_height'] = item_image.size

        return result

    @staticmethod
    def get_last_page_number(soup: BeautifulSoup):
        rightmost_arrow = soup.select_one("#paging > span:nth-child(12) > a.last")
        if rightmost_arrow is not None:
            return int(rightmost_arrow.attrs['onclick'][18:-3])
        return int(soup.select_one("#paging > a:last-child").text)
