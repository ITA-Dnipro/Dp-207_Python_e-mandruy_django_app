from datetime import datetime
import pytz


def api_route_time_converter(api_response):
    '''
    Return api_response route dict with changed datetime fields
    '''
    api_response['departure_date'] = datetime.strptime(
        api_response['departure_date'], '%d.%m.%Y'
    ).replace(hour=0, minute=0, second=0)
    #
    api_response['departure_date'] = pytz.timezone('Europe/Kiev').localize(
        api_response['departure_date'], is_dst=True
    )
    api_response['departure_date'] = (
        api_response['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    #
    api_response['parsed_time'] = datetime.strptime(
        api_response['parsed_time'], '%d-%m-%Y %H:%M:%S'
    )
    api_response['parsed_time'] = pytz.timezone('Europe/Kiev').localize(
        api_response['parsed_time'], is_dst=True
    )
    api_response['parsed_time'] = (
        api_response['parsed_time'].astimezone(pytz.timezone('UTC'))
    )
    return api_response


def api_cars_time_converter(api_response):
    '''
    Return api_response dict with changed datetime fields
    '''
    api_response['departure_date'] = datetime.strptime(
        api_response['departure_date'], '%d/%m/%Y %H:%M:%S'
    )
    api_response['departure_date'] = pytz.timezone('Europe/Kiev').localize(
        api_response['departure_date'], is_dst=True
    )
    api_response['departure_date'] = (
        api_response['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    #
    api_response['parsed_time'] = datetime.strptime(
        api_response['parsed_time'], '%d-%m-%Y %H:%M:%S'
    )
    api_response['parsed_time'] = pytz.timezone('Europe/Kiev').localize(
        api_response['parsed_time'], is_dst=True
    )
    api_response['parsed_time'] = (
        api_response['parsed_time'].astimezone(pytz.timezone('UTC'))
    )
    return api_response


def train_api_response_time_converter(api_response):
    '''
    Return api_response dict with changed datetime fields
    '''
    api_response['departure_date'] = datetime.strptime(
        api_response['departure_date'], '%d.%m.%Y'
    )
    api_response['departure_date'] = pytz.timezone('Europe/Kiev').localize(
        api_response['departure_date'], is_dst=True
    )
    api_response['departure_date'] = (
        api_response['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    #
    api_response['parsed_time'] = datetime.strptime(
        api_response['parsed_time'], '%d-%m-%Y %H:%M:%S'
    )
    api_response['parsed_time'] = pytz.timezone('Europe/Kiev').localize(
        api_response['parsed_time'], is_dst=True
    )
    api_response['parsed_time'] = (
        api_response['parsed_time'].astimezone(pytz.timezone('UTC'))
    )
    for train in api_response['trips']:
        #
        train['departure_date'] = datetime.strptime(
            train['departure_date'], '%Y-%m-%d %H:%M:%S'
        )
        train['departure_date'] = pytz.timezone('Europe/Kiev').localize(
            train['departure_date'], is_dst=True
        )
        train['departure_date'] = (
            train['departure_date'].astimezone(pytz.timezone('UTC'))
        )
        #
        train['arrival_date'] = datetime.strptime(
            train['arrival_date'], '%Y-%m-%d %H:%M:%S'
        )
        train['arrival_date'] = pytz.timezone('Europe/Kiev').localize(
            train['arrival_date'], is_dst=True
        )
        train['arrival_date'] = (
            train['arrival_date'].astimezone(pytz.timezone('UTC'))
        )
        #
        train['parsed_time'] = datetime.strptime(
            train['parsed_time'], '%d-%m-%Y %H:%M:%S'
        )
        train['parsed_time'] = pytz.timezone('Europe/Kiev').localize(
            train['parsed_time'], is_dst=True
        )
        train['parsed_time'] = (
            train['parsed_time'].astimezone(pytz.timezone('UTC'))
        )
    return api_response
