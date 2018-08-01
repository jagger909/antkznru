#-*- coding: utf-8 -*-
from django.conf import settings
from kik import user

from scheduler.models import Scheduler
class SchedulerManager(object):

    def add_sched(self, creds):
        user_name, address, telephone, comment, rep_date, rep_time = creds.split(':')
        print(user_name)
        # sched = Scheduler(username=user_name,
        #                   address=address,
        #                   telephone=telephone,
        #                   comment=comment,
        #                   repair_date=rep_date,
        #                   repair_time=rep_time, )
        # try:
        #     sched.save()
        # except ValueError:
        #     TelegramBot.sendMessage(chat_id, user_name)

    def get_sched(self):
        pass

    def get_event(self, bot, command, chat_id):
        main_comm = command
        if main_comm == 'add':
            self.add_sched(self, command[1])
        if main_comm == 'del':
            print(main_comm)
        if main_comm == 'upd':
            print(main_comm)