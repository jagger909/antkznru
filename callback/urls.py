from django.urls import path

from callback.views import CallBackView

urlpatterns = [
    path('', CallBackView.as_view(), name="callback_index"),
]
