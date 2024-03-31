import os


class ProcessChecker:
    def __init__(self):
        pass

    @staticmethod
    def is_processed_earlier(date: str):
        yyyymm, dd = date[:6], date[6:]
        filepath = f'log/process/{yyyymm}.log'
        if not os.path.exists(filepath):
            return False
        with open(filepath, 'r') as f:
            return dd in f.read().split(',')

    @staticmethod
    def check_as_processed(date: str):
        yyyymm, dd = date[:6], date[6:]
        filepath = f'log/process/{yyyymm}.log'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'a') as f:
            f.write(f'{dd},')
