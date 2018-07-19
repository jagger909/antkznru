from django.http import HttpResponse
from django.views.generic.base import TemplateView

from generic.mixins import CategoryListMixin


class MainPageView(TemplateView, CategoryListMixin):
    template_name = "main/mainpage.html"


    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        return context
