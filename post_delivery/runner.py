import json

from lambda_code.lambda_function import lambda_handler


def runner():
    lambda_handler({'origin': 'HaYarkon 20 tel aviv', 'destination': 'komoi 6 haifa', 'customer_id': 100},
        {})


if __name__ == '__main__':
    runner()
