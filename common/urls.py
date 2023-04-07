from django.urls import path
from common import views

urlpatterns = [
    path('feedback_list', views.feedback_list, name='feedback_list'),
    path('feedback_detail', views.feedback_detail, name='feedback_detail'),
    path('feedback_delete', views.feedback_delete, name='feedback_delete'),

    path('get_weather_data', views.get_weather_data, name='get_weather_data'),

]
