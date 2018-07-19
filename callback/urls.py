from django.urls import path

from callback.views import CallBackView, msg_send

urlpatterns = [
    path('', CallBackView.as_view(), name="callback_index"),
    path('msgsend/', msg_send, name="callback_msg_send"),
]
