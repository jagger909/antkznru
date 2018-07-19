from django.urls import path

from aboutus.views import AboutUsView

urlpatterns = [
    path('', AboutUsView.as_view(), name="aboutus_index"),
]
