from transport.models import Route, Car
from datetime import datetime  # , timedelta
import pytz
from django.forms.models import model_to_dict
from services.transport_app.api_utils.api_response_helpers import (
    api_route_time_converter,
    api_cars_time_converter
)
from services.transport_app.models_utils.route_helpers import (
    model_query_time_converter
)


def is_car_exists(payload):
    '''
    Return True if Car exists
    '''
    db_payload = dict(payload)
    db_payload = car_model_query_time_converter(db_payload)
    car = Car.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name']
    ).first()
    if car:
        return True
    return False


def is_car_has_same_departure_date_with_route(route_departure_date, car):
    '''
    Return True if car has same departure_date with route
    '''
    #
    car_payload = {}
    car_payload['departure_date'] = car['departure_date']
    car_payload = car_model_query_date_converter(
        car_payload
    )
    #
    route_date = route_departure_date
    car_date = car_payload['departure_date']
    #
    if route_date == car_date:
        return True
    return False


def save_api_response_in_route_and_car_models(api_response):
    '''
    Saving api_response dict in Route and Car models
    '''
    api_response = api_route_time_converter(api_response)
    route = Route.objects.create(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        parsed_time=api_response['parsed_time'],
        source_name=api_response['source_name'],
        source_url=api_response['source_url'],
    )
    for one_car in api_response['trips']:
        #
        same_car_and_route_derarture_date = (
            is_car_has_same_departure_date_with_route(
                route_departure_date=api_response['departure_date'],
                car=one_car
            )
        )
        #
        if same_car_and_route_derarture_date:
            #
            one_car = api_cars_time_converter(one_car)
            #
            Car.objects.create(
                route_id=route,
                departure_name=one_car['departure_name'],
                departure_date=one_car['departure_date'],
                arrival_name=one_car['arrival_name'],
                price=one_car['price'],
                car_model=one_car['car_model'],
                blablacar_url=one_car['blablacar_url'],
                parsed_time=one_car['parsed_time'],
                source_name=one_car['source_name'],
                source_url=one_car['source_url'],
            )


def update_api_response_in_route_and_car_models(api_response, source_name):
    '''
    Update Route and Car models rows
    '''
    api_response = api_route_time_converter(api_response)
    #
    Route.objects.filter(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        source_name=source_name,
    ).update(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        parsed_time=api_response['parsed_time'],
        source_name=api_response['source_name'],
        source_url=api_response['source_url'],
    )
    #
    route = Route.objects.filter(
        departure_name=api_response['departure_name'],
        departure_date=api_response['departure_date'],
        arrival_name=api_response['arrival_name'],
        source_name=source_name,
    ).first()
    for one_car in api_response['trips']:
        same_car_and_route_derarture_date = (
            is_car_has_same_departure_date_with_route(
                route_departure_date=api_response['departure_date'],
                car=one_car
            )
        )
        if same_car_and_route_derarture_date:
            #
            one_car = api_cars_time_converter(one_car)
            #
            db_car = Car.objects.filter(
                departure_name=one_car['departure_name'],
                departure_date=one_car['departure_date'],
                arrival_name=one_car['arrival_name'],
                price=one_car['price'],
                car_model=one_car['car_model'],
                blablacar_url=one_car['blablacar_url'],
                source_name=one_car['source_name'],
                source_url=one_car['source_url'],
            )
            if db_car.exists():
                db_car.update(
                    route_id=route,
                    departure_name=one_car['departure_name'],
                    departure_date=one_car['departure_date'],
                    arrival_name=one_car['arrival_name'],
                    price=one_car['price'],
                    car_model=one_car['car_model'],
                    blablacar_url=one_car['blablacar_url'],
                    parsed_time=one_car['parsed_time'],
                    source_name=one_car['source_name'],
                    source_url=one_car['source_url'],
                )
            else:
                db_car.create(
                    route_id=route,
                    departure_name=one_car['departure_name'],
                    departure_date=one_car['departure_date'],
                    arrival_name=one_car['arrival_name'],
                    price=one_car['price'],
                    car_model=one_car['car_model'],
                    blablacar_url=one_car['blablacar_url'],
                    parsed_time=one_car['parsed_time'],
                    source_name=one_car['source_name'],
                    source_url=one_car['source_url'],
                )


def car_model_query_time_converter(db_payload):
    '''
    Return payload dict with payload['departure_date'] converted
    to datetime object with proper timezone
    '''
    db_payload['departure_date'] = datetime.strptime(
        db_payload['departure_date'], '%d/%m/%Y %H:%M:%S'
    )
    db_payload['departure_date'] = pytz.timezone(
        'Europe/Kiev'
    ).localize(
        db_payload['departure_date'], is_dst=True
    )
    db_payload['departure_date'] = (
        db_payload['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    return db_payload


def car_model_query_date_converter(db_payload):
    '''
    Return payload dict with payload['departure_date'] converted
    to datetime object with just date
    '''
    db_payload['departure_date'] = datetime.strptime(
        db_payload['departure_date'], '%d/%m/%Y %H:%M:%S'
    )
    db_payload['departure_date'] = db_payload['departure_date'].replace(
        hour=0,
        minute=0,
        second=0
    )
    db_payload['departure_date'] = pytz.timezone(
        'Europe/Kiev'
    ).localize(
        db_payload['departure_date'], is_dst=True
    )
    db_payload['departure_date'] = (
        db_payload['departure_date'].astimezone(pytz.timezone('UTC'))
    )
    return db_payload


def get_cars_db_data(payload, source_name):
    db_payload = dict(payload)
    db_payload = model_query_time_converter(db_payload)
    route = Route.objects.filter(
        departure_name=db_payload['departure_name'],
        departure_date=db_payload['departure_date'],
        arrival_name=db_payload['arrival_name'],
        source_name=source_name,
    ).first()
    #
    if not route:
        db_response = {}
        db_response['result'] = False
        return db_response
    #
    db_response = model_to_dict(route)
    #
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    cars = [
        car for car in Car.objects.filter(
            route_id=route,
        ).filter(
            departure_date__gte=now_utc
        ).order_by(
            'departure_date'
        ).all().values()
    ]
    db_response['trips'] = cars
    db_response['result'] = True
    return db_response
