import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView
from django.views.generic.base import ContextMixin, TemplateView

from generic.controllers import PageNumberView
from generic.mixins import CategoryListMixin, PageNumberMixin
from telebot import telegram_send
from .forms import SchedulerForm
from .models import Scheduler

# Create your views here.


TIME_INDEX = {
    '08:00': 'T1',
    '10:00': 'T2',
    '12:00': 'T3',
    '14:00': 'T4',
    '16:00': 'T5',
    '18:00': 'T6',
    # '20:00': 'T7',
}


def scheduler_free_time(request):
    rep_date = datetime.date.today()

    # rep_date = datetime.datetime.strptime('09-06-2018', "%d-%m-%Y")
    num_days = 10
    filtered_sched = Scheduler.objects.filter(repair_date__range=(rep_date, rep_date + datetime.timedelta(days=num_days)))
    date_list = [rep_date + datetime.timedelta(days=x) for x in range(0, num_days)]
    events = {}
    for date in date_list:
        busy_time = []
        date_time_list = {choices.name: choices.value for choices in Scheduler.TimeChoice}

        # Уберем прошедшие окна на сегодняшний день.
        if date == datetime.date.today():
            time_now_minus_hour = datetime.datetime.now() + datetime.timedelta(hours=-1)
            for time_window in TIME_INDEX:
                if time_window < time_now_minus_hour.time().strftime('%H:%M'):
                    date_time_list.pop(TIME_INDEX[time_window])

        date_busy_time = filtered_sched.filter(repair_date=date)
        for time in date_busy_time:
            busy_time.append(time.repair_time)

        if busy_time:
            for time in busy_time:
                try:
                    date_time_list.pop(time)
                except:
                    pass

        if date_time_list:
            events[date.strftime('%d-%m-%Y')] = date_time_list
        if len(events) == 5:
            break

    output = {}
    output["busy_times"] = events

    return JsonResponse(output)


def scheduler_add(request):
    if request.method == 'POST':

        post_username = request.POST.get('post_username')
        post_address = request.POST.get('post_address')
        post_telephone = request.POST.get('post_telephone')
        post_comment = request.POST.get('post_comment')
        post_repair_date = request.POST.get('post_repair_date')
        post_repair_time = request.POST.get('post_repair_time')

        # Уже регистрировал заявку?
        if request.session.get('has_send', False):
            return JsonResponse({"response": "Вы уже записаны на ремонт. Свяжитесь с менеджером.", 'result': 'has_send', 'sched_un_id': post_un_id})

        # Проверка на свободность временного окна.
        filtered_sched = Scheduler.objects.filter(repair_date=post_repair_date, repair_time=post_repair_time)
        if filtered_sched:
            return JsonResponse({"response": "Дата уже занята.", 'result': 'error'})

        sched = Scheduler(username=post_username,
                          address=post_address,
                          telephone=post_telephone,
                          comment=post_comment,
                          repair_date=post_repair_date,
                          repair_time=post_repair_time, )
        try:
            sched.save()
        except ValueError:
            return JsonResponse({"response": "Не могу схранить заявку.", 'result': 'error'})

        message = "*ЗАЯВКА С САЙТА*:" + "\n" + "*ID*: " + sched.sched_un_id + "\n" + "*ИМЯ*: " + post_username + "\n" + "*ТЕЛЕФОН*: " + post_telephone + "\n" + "*АДРЕС*: " + post_address + "\n" + "*КОММЕНТАРИЙ*: " + post_comment + "\n" + "*ДАТА*: " + post_repair_date + "\n" + "*ВРЕМЯ*: " + getattr(
            Scheduler.TimeChoice, post_repair_time).value
        try:
            telegram_send.send_message(message)
        except:
            return JsonResponse({"response": "Не могу отправить заявку.", 'result': 'error'})

        request.session['has_send'] = True
        request.session['sched_un_id'] = sched.sched_un_id

        return JsonResponse({'response': "Заявка успешно добавлена", 'result': 'success', 'sched_un_id': sched.sched_un_id})


    else:
        return JsonResponse({'response': "Ты кто?", "error": "Not POST."})


class SortMixin(ContextMixin):
    sort = "0"
    order = "A"

    def get_context_data(self, **kwargs):
        context = super(SortMixin, self).get_context_data(**kwargs)
        context["sort"] = self.sort
        context["order"] = self.order
        return context


class SchedulerListView(PageNumberView, ListView, SortMixin, CategoryListMixin):
    model = Scheduler
    template_name = "scheduler/scheduler_list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.sched = Scheduler.objects.first()
        # logger.debug(self.cat.name)
        return super(SchedulerListView, self).get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(SchedulerListView, self).get_context_data(**kwargs)
    #
    #     return context

    def get_queryset(self):
        schedulers = Scheduler.objects.all()
        if self.sort == "2":
            if self.order == "D":
                schedulers = schedulers.order_by("-repair_date", "-repair_time")
            else:
                schedulers = schedulers.order_by("repair_date", "repair_time")
        elif self.sort == "1":
            if self.order == "D":
                schedulers = schedulers.order_by("-repair_date", "repair_time")
            else:
                schedulers = schedulers.order_by("repair_date", "-repair_time")
        else:
            if self.order == "D":
                schedulers = schedulers.order_by("-repair_time")
            else:
                schedulers = schedulers.order_by("repair_time")
        return schedulers


class SchedulerDetailView(PageNumberView, DetailView, SortMixin, PageNumberMixin):
    model = Scheduler
    template_name = "scheduler/sched.html"
    slug_field = 'sched_un_id'
    slug_url_kwarg = 'sched_un_id'


class SchedulerCreate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    template_name = "scheduler/scheduler_add.html"
    form = None
    sched = None

    # formset = None

    def get(self, request, *args, **kwargs):
        self.form = SchedulerForm()
        # self.formset = GoodImagesFormset()
        return super(SchedulerCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SchedulerCreate, self).get_context_data(**kwargs)
        context["form"] = self.form
        # context["formset"] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.form = SchedulerForm(request.POST, request.FILES)
        if self.form.is_valid():

            # Проверка на свободность временного окна.
            filtered_scheds = Scheduler.objects.filter(repair_date=self.form.cleaned_data['repair_date'], repair_time=self.form.cleaned_data['repair_time'])
            if filtered_scheds:
                messages.add_message(request, messages.ERROR, "Окно уже занято")
                return super(SchedulerCreate, self).get(request, *args, **kwargs)

            new_sched = self.form.save()
            # self.formset = GoodImagesFormset(request.POST, request.FILES, instance=new_good)
            # if self.formset.is_valid():
            #     self.formset.save()
            messages.add_message(request, messages.SUCCESS, "Заявка успешно добавлена")
            return redirect(
                reverse_lazy("scheduler_index") + "?page=" + self.request.GET["page"] + "&sort=" + self.request.GET["sort"] + "&order=" + self.request.GET["order"])

        return super(SchedulerCreate, self).get(request, *args, **kwargs)


class SchedulerUpdate(PageNumberView, TemplateView, SortMixin, PageNumberMixin):
    sched = None
    template_name = "scheduler/scheduler_edit.html"
    form = None

    # formset = None

    def get(self, request, *args, **kwargs):
        self.sched = Scheduler.objects.get(sched_un_id=self.kwargs["sched_un_id"])
        self.form = SchedulerForm(instance=self.sched)
        # self.formset = GoodImagesFormset(instance=self.good)
        return super(SchedulerUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SchedulerUpdate, self).get_context_data(**kwargs)
        # context["sched"] = self.sched
        context["form"] = self.form
        # context["formset"] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        self.sched = Scheduler.objects.get(sched_un_id=self.kwargs["sched_un_id"])
        self.form = SchedulerForm(request.POST, instance=self.sched)
        # self.formset = GoodImagesFormset(request.POST, request.FILES, instance=self.good)
        if self.form.is_valid():
            self.form.save()
            messages.add_message(request, messages.SUCCESS, "Заявка успешно изменена")
            return redirect(reverse_lazy("scheduler_index") + "?page=" + self.request.GET["page"] + "&sort=" + self.request.GET["sort"] + "&order=" + self.request.GET["order"])
        return super(SchedulerUpdate, self).get(request, *args, **kwargs)


class SchedulerDelete(PageNumberView, DeleteView, SortMixin, PageNumberMixin):
    model = Scheduler
    template_name = "scheduler/scheduler_delete.html"

    slug_url_kwarg = 'sched_un_id'
    slug_field = 'sched_un_id'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse_lazy("scheduler_index") + "?page=" + self.request.GET["page"] + "&sort=" + self.request.GET["sort"] + "&order=" + self.request.GET["order"]
        messages.add_message(request, messages.SUCCESS, "Заявка успешно удалена")
        return super(SchedulerDelete, self).post(request, *args, **kwargs)
