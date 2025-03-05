import json

def response_status(code, message):
    """ Default response. """

    try:
        body = json.dumps(message, sort_keys=True)
    except json.decoder.JSONDecodeError:
        body = message

    response = {
        'statusCode': code,
        'body': body
    }

    return response
