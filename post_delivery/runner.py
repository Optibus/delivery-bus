import json

from lambda_code.lambda_function import lambda_handler


def runner():
    lambda_handler(
        {
            "check_id": 1827179,
            "check_name": "Name of HTTP check",
            "check_type": "HTTP",
            "check_params": {
                "basic_auth": False,
                "encryption": True,
                "full_url": "https://www.example.com/path",
                "header": "User-Agent:Pingdom.com_bot",
                "hostname": "www.example.com",
                "ipv6": False,
                "port": 443,
                "url": "/path"
            },
            "tags": [
                "example_tag"
            ],
            "previous_state": "UP",
            "current_state": "DOWN",
            "importance_level": "HIGH",
            "state_changed_timestamp": 1451610061,
            "state_changed_utc_time": "2016-01-01T01:01:01",
            "long_description": "Long error message",
            "description": "Short error message",
            "first_probe": {
                "ip": "123.4.5.6",
                "ipv6": "2001:4800:1020:209::5",
                "location": "Stockholm, Sweden"
            },
            "second_probe": {
                "ip": "123.4.5.6",
                "ipv6": "2001:4800:1020:209::5",
                "location": "Austin, US",
                "version": 1
            }
        },
        {})


if __name__ == '__main__':
    runner()
