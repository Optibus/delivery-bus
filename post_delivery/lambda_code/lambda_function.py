from __future__ import print_function

import json

print('Loading function')


def response(res=None):
    return {
        'statusCode': '200',
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    check_id = event.get('check_id')
    check_name = event.get('check_name')
    if check_id is None:
        return response({'ERROR': 'No check ID'})

    cls = pingdom_checks.get(check_id)
    if cls is None:
        return response({'ERROR': 'Check {} (id: {}) is not registered'.format(check_name, check_id)})

    return response(cls().handle_check(event))
