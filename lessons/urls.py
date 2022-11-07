from django.urls import path
from lessons import views

urlpatterns = [
    # path('lesson_list', views.lesson_list, name='lesson_list')
    path('homework_code', views.homework_code, name='homework_code'),
    path('compile_code', views.compile_code, name='compile_code'),

]
