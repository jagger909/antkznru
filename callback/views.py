from django.views.generic.base import TemplateView
from generic.mixins import CategoryListMixin
from django.http import HttpRequest

class CallBackView(TemplateView, CategoryListMixin):
    template_name = "callback/appointment.html"


def sms_send(msg):
    url = "http://sms.ru/sms/send?api_id=%(api_id)s&to=%(to)s&text=%(msg)s"
    id_api = "AFAA4570-8FEE-0ADA-7EBE-781D7A61B515"
    number = "9179354824"
    urlToSend = url % {'api_id': id_api, 'to': number, 'msg': msg.encode('utf-8')}
    res = HttpRequest.POST(urlToSend)
    res = res.code


    return 'SMS status: %s' % res