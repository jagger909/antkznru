from django.contrib.auth.decorators import permission_required
from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.scheduler_add, name="sched_add"),
    path('get_scheds/', views.scheduler_free_time, name="scheduler_get"),
    path('', permission_required("scheduler.view_scheds")(views.SchedulerListView.as_view()), name="scheduler_index"),
    path('<slug:sched_un_id>/detail/', permission_required("scheduler.detail_sched")(views.SchedulerDetailView.as_view()), name="scheduler_detail"),
    path('sched_add/', permission_required("scheduler.add_sched")(views.SchedulerCreate.as_view()), name="scheduler_add"),
    path('<slug:sched_un_id>/edit/', permission_required("scheduler.change_sched")(views.SchedulerUpdate.as_view()), name="scheduler_edit"),
    path('<slug:sched_un_id>/delete/', permission_required("scheduler.delete_sched")(views.SchedulerDelete.as_view()), name="scheduler_delete"),
]
