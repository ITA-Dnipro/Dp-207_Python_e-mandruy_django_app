from django.urls import path
from . import views
from .api_views import TransportApiView


app_name = 'transport'

urlpatterns = [
    path('', views.main_view, name='main_view'),
    path('<route_name>/', views.route_view, name='route_view'),
    path(
        'schedule',
        views.schedule_post_handler,
        name='schedule_post_handler'
    ),
    path('api/v1/get_routes',
         TransportApiView.as_view(),
         name='routes_api')

]
