from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.scheduler_view, name="scheduler_index"),
    path('', views.SchedulerView.as_view()),
    path('add/', views.scheduler_add, name="scheduler_add"),
    path('get_scheds/', views.scheduler_free_time, name="scheduler_add"),
]
