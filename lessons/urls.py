from django.urls import path
from lessons import views

urlpatterns = [
    path('exercises_detail', views.exercises_detail, name='exercises_detail'),
    path('homework_code', views.homework_code, name='homework_code'),
    path('compile_code', views.compile_code, name='compile_code'),

]
