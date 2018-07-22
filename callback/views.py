from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from telebot import telegram_send



class CallBackView(TemplateView, CategoryListMixin):
    template_name = "callback/appointment.html"


def msg_send(request):

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        question_text = request.POST.get('question_text')
        user_name = request.POST.get('user_name')

        message = "*ВОПРОС С САЙТА*:" + "\n" + "*ИМЯ*: " + user_name + "\n" + "*ТЕЛЕФОН*: " + phone_number + "\n" + "*КОММЕНТАРИЙ*: " + question_text
        telegram_send.send_message(message)

        return HttpResponseRedirect(reverse_lazy('main'))

    else:
        return HttpResponseRedirect(reverse_lazy('main'))

