# -*- coding: utf8 -*-

import json
import logging

import telepot
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from kik.messages import keyboards
from telegram import inlinekeyboardbutton, inlinekeyboardbutton
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from .utils import planet_parser, scheduler

logger = logging.getLogger('telegram.bot')


def _display_help():
    markup = ReplyKeyboardMarkup(keyboard=[
        [dict(text='Инфо')],
        [dict(text='Управление')],
        [dict(text='Заявки')],
    ])
    return markup, render_to_string('telebot/help.md')


def _display_start():
    markup = ReplyKeyboardMarkup(keyboard=[
        [dict(text='Инфо')],
        [dict(text='Управление')],
        [dict(text='Заявки')],
    ])
    msg = 'Выбери раздел'
    return markup, msg


def _display_main_menu():
    markup = ReplyKeyboardMarkup(keyboard=[
        [dict(text='Инфо')],
        [dict(text='Управление')],
        [dict(text='Заявки')],
    ])
    msg = 'Выбери раздел'

    return markup, msg


def _display_info():
    markup = ReplyKeyboardMarkup(keyboard=[
        [dict(text='Сервер'), dict(text='Сайт')],
        [dict(text='Главное_меню')],
    ])
    msg = 'Выбери объект'
    return markup, msg


def _display_info_server():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Текст 1', callback_data='command-one')],
        [InlineKeyboardButton(text='url', url='https://antkzn.ru')],
    ])
    msg = 'Выбери объект'
    return markup, msg


def _display_info_site():
    markup = ReplyKeyboardMarkup(keyboard=[
        [dict(text='Сервер'), dict(text='Сайт')],
        [dict(text='Главное_меню')],
    ])
    msg = 'Выбери объект'
    return markup, msg


def _display_sched_events():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Заявки сегодня', callback_data='event_today')],
        [InlineKeyboardButton(text='Заявки завтра', callback_data='event_tomorrow')],
    ])

    msg = 'Выбери действие'
    return markup, msg

def _display_scheduler():
    markup = ReplyKeyboardMarkup(keyboard=[
        [dict(text='События'), dict(text='Управление_заявками')],
        [dict(text='Главное_меню')],
    ])
    msg = 'Выбери действие'
    return markup, msg

def _display_scheduler_manager():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Текст 1', callback_data='command-one')],
        [InlineKeyboardButton(text='url', url='https://antkzn.ru')],
    ])
    msg = 'Выбери объект'
    return markup, msg

def _display_planetpy_feed():
    return render_to_string('telebot/feed.md', {'items': planet_parser.parse_planetpy_rss()})


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)
sched_manager = scheduler.SchedulerManager()


class CommandReceiveView(View):

    #
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')
        commands = {
            'help': _display_help,
            'feed': _display_planetpy_feed,
            'start': _display_start(),
            'главное_меню': _display_main_menu(),
            'инфо': _display_info(),
            'сервер': _display_info_server(),
            'заявки': _display_scheduler(),
            'события': _display_sched_events(),
            'управление_заявками': _display_scheduler_manager(),
        }

        try:
            payload = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')

        if 'message' in payload:
            msg = payload['message']
            content_type, chat_type, chat_id = telepot.glance(msg)
            text = msg['text']
            print('Text:', text)

            cmd = text.split()  # command
            clr_cmd = cmd[0].lower()
            func = commands.get(clr_cmd)
            if func:
                markup, render = func
                TelegramBot.sendMessage(chat_id, render, parse_mode='Markdown', reply_markup=markup)
            elif clr_cmd == 'scheds':
                ressponse = sched_manager.get_event(self, cmd[1:], chat_id)
            else:
                TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')

        elif 'callback_query' in payload:
            msg = payload['callback_query']
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            print('Callback Query:', query_id, from_id, query_data)

            TelegramBot.answerCallbackQuery(query_id, text=query_data, show_alert=True)

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
