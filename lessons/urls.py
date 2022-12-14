from django.urls import path
from lessons import views

urlpatterns = [
    path('exercises_detail', views.exercises_detail, name='exercises_detail'),
    path('homework_code', views.homework_code, name='homework_code'),
    path('compile_code', views.compile_code, name='compile_code'),
    path('attendance_list', views.attendance_list, name='attendance_list'),
    path('lesson_list', views.lesson_list, name='lesson_list'),
    path('lesson_status_change', views.lesson_status_change, name='lesson_status_change'),
    path('lesson_delete', views.lesson_delete, name='lesson_delete'),

]
