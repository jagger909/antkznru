#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
from importlib import reload

import telepot, random, os, sys
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from pprint import *
import random, time

#message_with_inline_keyboard = None
######### UTF8 ########
os.system("clear")
reload(sys)

#sys.setdefaultencoding('utf8')


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    try:
        a = msg['chat']['title']
    except:
        a = msg['chat']['id']
    b = content_type
    c = chat_type
    d = chat_id
    texto = msg['text']

    nome = msg['from']['first_name']
    id = msg['from']['id']
    send = bot.sendMessage
    from_id = msg['from']['id']
    chat_id = msg['chat']['id']
    master = msg['from']['id']
    reply_msg = "reply_to_message_id=msg['message_id']"
    txt = msg['text'].split(' ')
    message = msg['text'].split()
    len_msg = len(message)
    msg_id = msg['message_id']
    M = "Markdown"
    print(msg['text'], msg['chat']['id'])

    #############################
    # COMANDOS
    #############################
    if texto == '/menu':
        markup = ReplyKeyboardMarkup(keyboard=[['OCULTAR', KeyboardButton(text='MEU CANAL')], [dict(text='INFO', callback_data='info'), KeyboardButton(text='GITHUB')], ])
        bot.sendMessage(chat_id, 'Menú extra!', reply_markup=markup)
    elif txt[0].lower() == '/go':
        if (from_id == seu - id):  ####coloque seu-id
            if len_msg > 1:
                texto = msg[u'text'].split(' ', 1)[1]
                bot.sendMessage(chat_id, 'σk, vσu єnvíαr....')
                try:
                    bot.sendMessage(-1001106487387, texto, parse_mode="Markdown")
                except:
                    try:
                        bot.sendMessage(-1001106487387, texto)
                    except:
                        bot.sendMessage(chat_id, "αlgσ єѕtα ímpєdíndσ quє єu єnvíє, pσr fαvσr vєrífíquє...", reply_to_message_id=msg["message_id"])

                bot.sendMessage(chat_id, 'mєnѕαgєm єnvíαdα!', reply_to_message_id=msg["message_id"])
    elif texto == "MEU CANAL":
        markup = ReplyKeyboardMarkup(keyboard=[['OCULTAR', KeyboardButton(text='MEU CANAL')], [dict(text='INFO'), KeyboardButton(text='GITHUB')], ])
        bot.sendMessage(chat_id, '[{}](telegram.me/{})'.format('Robo taylor', 'robotaylor', ), parse_mode=M, disable_web_page_preview=True, reply_markup=markup, reply_to_message_id=msg_id)
    elif texto == 'GUITHUB':
        bot.sendMessage(chat_id, "https://github.com/francis-taylor/botlist")
    elif texto == 'INFO':
        a = bot.getMe()
        n = a['first_name']
        u = a['username']

        bot.sendMessage(chat_id, '''
🤖Informações do bot:
*________________________*
bot: {}
username: {}
*_________*
by [cyon](https://telegram.me/robotaylor) '''.format(n, u), parse_mode=M)
    elif texto == '/chat_id':
        bot.sendMessage(chat_id, chat_id)
    elif txt[0] == '/adicione':
        if (from_id == 263799625) or (from_id == 259979813):
            if len_msg > 1:
                texto = msg[u'text'].split(' ', 1)[1]
                try:
                    arq = open('/root/lista.txt', 'a')
                except:
                    arq = open('/root/lista.txt', 'w')
                arq.write('• ' + texto + '\n')
                bot.sendMessage(chat_id, '_lista αtuαlízαdα!_', parse_mode="Markdown")
                arq.close()
        else:
            bot.sendMessage(chat_id, 'pєrmíѕѕãσ nєgαdα', reply_to_message_id=msg['message_id'])
    elif texto == '/lista':
        if (msg['chat']['type'] == 'private'):
            try:
                arq = open('/root/lista.txt', 'r')
            except:
                bot.sendMessage(chat_id, 'ѕєm ínfσrmαçõєѕ dєfínídαѕ...', parse_mode="Markdown")
            texto = arq.read()
            line = msg['chat']['id']
            regras = [chat_id, texto]
            id = regras[0]
            arq.close()
            for id in texto:
                bot.sendMessage(chat_id, '''
*Lista de canais disponíveis*📖

{}

_deseja adicionar seu canal na lista?
fale com_ @paulo6'''.format(texto), parse_mode="Markdown")
                break
        else:
            bot.sendMessage(chat_id, 'Comando apenas para privado..', reply_to_message_id=msg['message_id'])

    elif texto == 'GITHUB':
        bot.sendMessage(chat_id, '[Cyon robots](https://github.com/francis-taylor/cyon)', parse_mode=M)
    elif texto == '/start':
        bot.sendMessage(chat_id, 'Ok! Vamos começar!, aguenta só um pouquinho que ja vou te passar o menú...')
        time.sleep(2)
        markup = InlineKeyboardMarkup(inline_keyboard=[[dict(text='🔧suporte', url='https://telegram.me/robotaylor')],
                                                       [InlineKeyboardButton(text='📃status', callback_data='n')] + [InlineKeyboardButton(text='⚙Comandos', callback_data='edit')] + [
                                                           InlineKeyboardButton(text='ℹinfo', callback_data='info')]])
        global message_with_inline_keyboard
        message_with_inline_keyboard = bot.sendMessage(chat_id,
                                                       'Oin! prazer *{}*✌😄!\n`sou o` *{}*!\n\n`você pode ultilizar meus` *comandos*, `para conhecê-los, basta clicar no botão...`'.format(nome, name),
                                                       reply_markup=markup, parse_mode="Markdown")
    elif texto == 'OCULTAR':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'menu ocultado...', reply_markup=markup)
    elif texto == '/desbug':
        markup = ForceReply()
        bot.sendMessage(chat_id, 'Force reply', reply_markup=markup)
    elif msg['text'] == '/help':
        markup = InlineKeyboardMarkup(inline_keyboard=[[dict(text='📡Meu canal', url='https://telegram.me/joinchat/AAAAAEKOnI7Y4OULSopvOQ')],
                                                       [InlineKeyboardButton(text='👤Adms', callback_data='adm')] + [InlineKeyboardButton(text='👥grupo', callback_data='edit')],
                                                       [InlineKeyboardButton(text='🛠 remover usuário', callback_data='ban')] + [dict(text='Link🌐', callback_data='link')],
                                                       [InlineKeyboardButton(text='extras 🕹', callback_data='extra')] + [InlineKeyboardButton(text='📝Sobre o grupo', callback_data='sobre')],
                                                       [InlineKeyboardButton(text='⚙DEVS', callback_data='dev')]])
        #global message_with_inline_keyboard
        mark = InlineKeyboardMarkup(inline_keyboard=[[dict(text='Iniciar conversa👤', url='https://telegram.me/{}?start'.format(config.user))]])
        try:
            message_with_inline_keyboard = bot.sendMessage(from_id, """
Deixa eu te fala, você pode entrar em contato com a minha equipe, a (equipe cyon)[t.me/robotaylor], lá eles oferecem suporte rsrs.""".format(msg['from']['first_name']), reply_markup=markup,
                                                           parse_mode="Markdown")
        except:
            bot.sendMessage(chat_id, 'Por favor inicie uma conversa privada primeiro e tente /help novamente', reply_markup=mark)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    if data == 'n':
        bot.answerCallbackQuery(query_id, text='estou ativo!')

    elif data == 'edit':
        global message_with_inline_keyboard
        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            markup = InlineKeyboardMarkup(inline_keyboard=[[dict(text='🔧suporte', url='https://telegram.me/robotaylor')],
                                                           [InlineKeyboardButton(text='📃status', callback_data='n')] + [InlineKeyboardButton(text='⚙', callback_data=' ')] + [
                                                               InlineKeyboardButton(text='ℹinfo', callback_data='info')]])

            bot.editMessageText(msg_idf, '''
rs, meus comandos desponíveis😊👇
*lista* - envia a lista de canais disponíveis.
*menu* - menu extra.

ultilize /<comando> para ultilizar o comando desejado.
EXEMPLO: */lista*''', parse_mode="Markdown", reply_markup=markup)
    elif data == 'info':
        a = bot.getMe()
        n = a['first_name']
        u = a['username']
#        global message_with_inline_keyboard
        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            markup = InlineKeyboardMarkup(inline_keyboard=[[dict(text='🔧suporte', url='https://telegram.me/robotaylor')],
                                                           [InlineKeyboardButton(text='📃status', callback_data='n')] + [InlineKeyboardButton(text='⚙Comandos', callback_data='edit')] + [
                                                               InlineKeyboardButton(text='ℹ', callback_data=' ')]])
            bot.editMessageText(msg_idf, '''
🤖*Informações do bot:*
➖➖➖➖➖➖➖➖➖
*bot*: `{}`

*username:*` {}`
➖➖➖➖
by [cyon](https://telegram.me/robotaylor) '''.format(n, u), disable_web_page_preview=True, parse_mode="Markdown", reply_markup=markup)


        else:
            bot.answerCallbackQuery(query_id, text='Ops! ocorreu um bug! tente /start....')


############# END ###############
bot = telepot.Bot("TOKEN")  ####token  bot
pprint("obtendo dados.....")

a = bot.getMe()
name = a['first_name']
pprint("Obtendo infos...")

pprint("ok!")
os.system("clear")
reload(sys)

answerer = telepot.helper.Answerer(bot)
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})

print(name + " Iniciado...")

# Keep the program running.

while 1:
    time.sleep(10)

