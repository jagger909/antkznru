import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from scheduler import telegram_send
from .forms import SchedulerForm
from .models import Scheduler


# Create your views here.


def scheduler_view(request):
    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = SchedulerForm(request.POST)
        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            # (здесь мы просто присваиваем их полю due_back)
            # book_inst.due_back = form.cleaned_data['renewal_date']
            # book_inst.save()
            form.save()
            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('main'))
    # Если это GET (или какой-либо еще), создать форму по умолчанию.
    else:
        form = SchedulerForm()

    return render(request, 'scheduler/scheduler.html', {'form': form})


class SchedulerView(CreateView):
    success_url = reverse_lazy('scheduler_index')
    form_class = SchedulerForm
    template_name = 'scheduler/scheduler2.html'

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

        post_un_id = request.POST.get('post_un_id')
        post_username = request.POST.get('post_username')
        post_address = request.POST.get('post_address')
        post_telephone = request.POST.get('post_telephone')
        post_comment = request.POST.get('post_comment')
        post_repair_date = request.POST.get('post_repair_date')
        post_repair_time = request.POST.get('post_repair_time')

        if request.session.get('has_send', False):
            return JsonResponse({"response": "Вы уже записаны на ремонт. Свяжитесь с менеджером.", 'result': 'has_send', 'sched_un_id': post_un_id})

        # Проверка на свободность временного окна.
        filtered_sched = Scheduler.objects.filter(repair_date=post_repair_date, repair_time=post_repair_time)
        if filtered_sched:
            return JsonResponse({"response": "Дата уже занята.", 'result': 'error'})

        message = "*ЗАЯВКА С САЙТА*:" + "\n" + "*ИМЯ*: " + post_username + "\n" + "*ТЕЛЕФОН*: " + post_telephone + "\n" + "*АДРЕС*: " + post_address + "\n" + "*КОММЕНТАРИЙ*: " + post_comment + "\n" + "*ДАТА*: " + post_repair_date + " " + post_repair_time
        telegram_send.send_message(message)


        sched = Scheduler(username=post_username,
                          address=post_address,
                          telephone=post_telephone,
                          comment=post_comment,
                          repair_date=post_repair_date,
                          repair_time=post_repair_time,
                          sched_un_id=post_un_id)
        try:
            sched.save()
        except ValueError:
            return JsonResponse({"response": "Не могу схранить заявку.", 'result': 'error'})
        
        request.session['has_send'] = True
        request.session['sched_un_id'] = post_un_id

        return JsonResponse({'response': "Заявка успешно добавлена", 'result': 'success', 'sched_un_id': post_un_id})


    else:
        return JsonResponse({'response': "Ты кто?", "error": "Not POST."})
