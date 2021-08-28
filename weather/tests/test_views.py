from django.test import TestCase
from django.urls import reverse
from unittest import mock
from django.http import HttpRequest
from django.test import Client

from weather.utils.logic import WeatherHandler
from weather.test_data.weather_data import CITY, WEATHER_DATA
from weather.models import Weather
from hotels.models import City
from weather.views import main_weather, get_weather_in_city


class MainWeatherViewTest(TestCase):

    def test_main_weather_view_url_exists_at_desired_location(self):
        response = self.client.get('/weather/main')

        self.assertEqual(response.status_code, 200)

    def test_main_weather_view_url_accessible_by_name(self):
        response = self.client.get(reverse('weather:main'))

        self.assertEqual(response.status_code, 200)

    def test_main_weather_view_uses_correct_template(self):
        response = self.client.get(reverse('weather:main'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/main_weather.html')


class GetWeatherInCityViewTest(TestCase):

    def setUp(self):
        c = Client()

    @mock.patch('weather.views.get_weather_in_city', side_effect=WEATHER_DATA)
    def test_get_weather_in_city_view(self, mock, city=CITY['city_name']):
        instance = WeatherHandler(city)
        instance.get_weather_from_api_and_create_model()

        self.assertTrue(City.objects.get(name=city))
        self.assertEqual(len(Weather.objects.all()), 4)

    def test_get_weather_in_city_view_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['city'] = 'Kyiv'
        response = get_weather_in_city(request)

        self.assertContains(response, request.POST['city'])

    def test_get_weather_in_city_view_url_exists_at_desired_location(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['city'] = 'Kyiv'
        response = get_weather_in_city(request)

        self.assertEqual(response.status_code, 200)
