from datetime import datetime, timedelta


class DatePicker:
    def __init__(self):
        self.start_date = datetime.today()
        self.end_date = datetime.today()

    def __len__(self):
        return (self.end_date - self.start_date).days + 1

    def input_data(self):
        default_input = datetime.today().strftime("%Y%m%d")
        print(f'시작 날짜 입력 [default={default_input}]')
        start_input = input() or default_input
        print(f'종료 날짜 입력 [default={default_input}] (종료 날짜까지 포함)')
        end_input = input() or default_input

        if start_input > end_input:
            raise ValueError('invalid date format')

        try:
            self.start_date = datetime.strptime(start_input, '%Y%m%d')
            self.end_date = datetime.strptime(end_input, '%Y%m%d')
            if self.end_date > datetime.today():
                raise ValueError()
        except ValueError:
            raise ValueError('invalid date format')

    def range(self):
        date_generated = [self.start_date + timedelta(days=x) for x in
                          range(0, (self.end_date - self.start_date).days + 1)]
        for date in date_generated:
            yield date.strftime('%Y%m%d')
