from django.urls import path

from contacts.views import ContactsView

urlpatterns = [
    path('', ContactsView.as_view(), name="contact_index"),
]
