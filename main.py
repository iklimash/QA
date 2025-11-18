import telebot
from aiogram.types import user
from telebot import types
from telebot.types import LabeledPrice
from telebot import util
import sqlite3
import random
import datetime
from yookassa import Configuration, Payment
import threading
import time
import test
import warnings
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Нужно сделать:
# - Оформить в Юмани официальный счет и заменить его вместо тестового
# - Выгрузить на хостинг + узнать, всё ли из этого кода будет работать правильно на сервере
# - Переписать на асинхрон ипостроить архитектуру


user_id = 0
email_id = 0
bot = telebot.TeleBot('7600122980:AAF1oUj0j2MMguDnRqAXzMppwUsVwiZPLkU')

payment_token = "381764678:TEST:131548"
Configuration.account_id = '1126365'
Configuration.secret_key = 'test_ntguItWM5ulclymmIKxoLEvENKY3iTvrMDdtewnGf8I'

warnings.filterwarnings("ignore")
# ТАСКИ
# Инструкция
# Разобарться с реальной оплатой в ю касс написать что доступ к серверу и еще че то там и отправить скириншот анкета подключения.

active_payments = {}

conn = sqlite3.connect('PandaVPN.sql')
cur = conn.cursor()
cur.execute('''
          CREATE TABLE IF NOT EXISTS users (
              user_id INTEGER PRIMARY KEY,
              expiry_end TIMESTAMP,
              main_used BOOLEAN DEFAULT FALSE
          )
          ''')
conn.commit()

# Автоматически подтверждает платежи в тестовом режиме
def auto_confirm_payments(days_payment):
    while True:
        for payment_id, data in list(active_payments.items()):
            try:
                payment = Payment.find_one(payment_id)

                if payment.status == "waiting_for_capture":
                    # Автоподтверждение платежа
                    Payment.capture(payment_id)
                    active_payments[payment_id]["status"] = "succeeded"
                    test.access(data["user_id"], days_payment)

                    bot.send_message(
                        data["user_id"],
                        "🐼 Платеж автоматически подтвержден!"

                    )

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    btn1 = types.InlineKeyboardButton('Инструкция', url='https://telegra.ph/Panda-VPN-Instrukciya-po-podklyucheniyu-07-29')
                    btn2 = types.InlineKeyboardButton('Основной период', callback_data='main_period')
                    btn3 = types.InlineKeyboardButton('Личный кабинет', callback_data='personal_account')
                    markup.add(btn1, btn2, btn3)

                    bot.send_message(data["user_id"], f'''ВПН доступен до: {test.get_expiry_time(user_id)} 

Ваша ссылка (копируется при нажатии): <code>{test.send_link(user_id)}</code>''',
                    reply_markup=markup, parse_mode='HTML')
                    
                elif payment.status == "succeeded" and data["status"] != "succeeded":
                    active_payments[payment_id]["status"] = "succeeded"
                    bot.send_message(
                        data["user_id"],
                        "💰 Платеж завершен! Доступ к VPN активирован."
                    )

                elif payment.status == "canceled":
                    bot.send_message(
                        data["user_id"],
                        "❌ Платеж отменен"
                    )
                    del active_payments[payment_id]

            except Exception as e:
                print(f"Ошибка: {e}")

        time.sleep(10)  # Проверка каждые 30 секунд

# Проверка состояния подписки и отправление уведомлений пользователя, что она заканчивается (закончилась)
# 
# берем все айди из базы данных, проверяем с помощью функций из test.py время окончания функции
# Если возвращает true, то отправляем соответствующее сообщение пользователю.
# в цикле for user_id in cur.fetchall() данные возвращаются в виде (18312758, ), (13251325, ). Поэтому пишем user_id[0]
def check_subscriptions():
    conn = sqlite3.connect('PandaVPN.sql')
    cur = conn.cursor()

    cur.execute('''SELECT user_id FROM users''')

    for user_id in cur.fetchall():
        if test.check_subscriptions_less_1_day(user_id[0]):
            with open('media/panda_sidit.mp4', 'rb') as video:
                bot.send_video(user_id[0], video = video,
                                 caption = "🐼 До окончания подписки остался 1 день! Продлите вовремя")
        if test.check_subscriptions_less_0_day(user_id[0]):
            with open('media/panda_angry.mp4', 'rb') as video:
                bot.send_video(user_id[0], video=video,
                               caption="🐼 Ваша подписка закончилась (")

# Проверяем состояние подписки каждый день
def background_checker_subscriptions():
    while True:
        check_subscriptions()
        time.sleep(24*3600)  # Проверка каждый день (24*3600 секунд)


@bot.message_handler(commands=['start'])
def start(message):
    global user_id
    user_id = message.from_user.id

    conn = sqlite3.connect('PandaVPN.sql')
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Инструкция', url='https://telegra.ph/Panda-VPN-Instrukciya-po-podklyucheniyu-07-29')
    btn2 = types.InlineKeyboardButton('Основной период', callback_data='main_period')
    btn3 = types.InlineKeyboardButton('Личный кабинет', callback_data='personal_account')
    markup.add(btn1, btn2, btn3)

    if not cur.fetchone():
        cur.execute('''
                    INSERT INTO users (user_id)
                    VALUES (?)
                ''', (user_id,))
        conn.commit()
        with open("media/panda_start.mp4", 'rb') as video:
            bot.send_video(message.chat.id, video = video, caption='''🐼 <b>Привет! Вижу ты здесь в первый раз</b>
                           
Мы хотим сделать тебе подарок: доступ к VPN на 7 дней. Ничего платить и регистрировать не нужно, просто скопируй ссылку и следуй инструкции ниже ''',
                            parse_mode='HTML')
        bot.send_message(message.chat.id, f'''<b>Вот ссылка, сохрани её (копируется при нажатии):</b> <code>{test.get_link(str(user_id),7)}</code>

<b>Открой 👇</b>''', reply_markup=markup, parse_mode='HTML')
    
    # Если пользователь уже получил ссылку, то выдаем навигацию
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Инструкция', url='https://telegra.ph/Panda-VPN-Instrukciya-po-podklyucheniyu-07-29')
        btn2 = types.InlineKeyboardButton('Основной период', callback_data='main_period')
        btn3 = types.InlineKeyboardButton('Личный кабинет', callback_data='personal_account')
        markup.add(btn1, btn2, btn3)

        bot.send_message(
            message.chat.id,
            '''<b>ГЛАВНОЕ МЕНЮ</b> 👋''',
            reply_markup=markup,
            parse_mode='HTML'
        )

    cur.close()
    conn.close()

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global user_id
    user_id = call.message.chat.id
    if call.data == 'main_period':
        markup = types.InlineKeyboardMarkup(row_width=2)

        btn_1_month = types.InlineKeyboardButton('1 месяц (99 руб)', callback_data='main_period_1_month')
        btn_3_month = types.InlineKeyboardButton('3 месяца (249 руб)', callback_data='main_period_3_month')
        btn_6_month = types.InlineKeyboardButton('6 месяцев (399 руб)', callback_data='main_period_6_month')
        btn_12_month = types.InlineKeyboardButton('12 месяцев (699 руб)', callback_data='main_period_12_month')
        markup.add(btn_1_month, btn_3_month, btn_6_month, btn_12_month)
        bot.send_message(
            call.message.chat.id,
            '''<b>Выберите тариф:</b>''',
            reply_markup=markup,
            parse_mode='HTML'
        )


    elif call.data == 'personal_account':

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Инструкция', url='https://telegra.ph/Panda-VPN-Instrukciya-po-podklyucheniyu-07-29')
        btn2 = types.InlineKeyboardButton('Основной период', callback_data='main_period')

        markup.add(btn1, btn2)

        bot.send_message(call.message.chat.id,
                         f'''🐼 <b>ЛИЧНЫЙ КАБИНЕТ</b>

ВПН доступен до: {test.get_expiry_time(user_id)}

Ваша ссылка (копируется при нажатии): <code>{test.send_link(user_id)}</code>
''',
                        reply_markup=markup, parse_mode='HTML')

    elif call.data == 'main_period_1_month':

        thread = threading.Thread(target=auto_confirm_payments, args=(30,))
        thread.daemon = True
        thread.start()

        payment = Payment.create({
            "amount": {"value": "99.00", "currency": "RUB"},
            "capture": False,  # Важно для ручного подтверждения
            "confirmation": {"type": "redirect", "return_url": "https://t.me/PandaVPN_tg_bot"},
            "description": "VPN подписка",
            "metadata": {"user_id": user_id},
        })

        active_payments[payment.id] = {
            "user_id": user_id,
            "status": "pending"
        }

        bot.send_message(
            call.message.chat.id,
            f"🐼 Ссылка для оплаты:\n{payment.confirmation.confirmation_url}\n\n"
            "Доступ придет автоматически в течение 1 минуты после оплаты!"
        )
    elif call.data == 'main_period_3_month':

        thread = threading.Thread(target=auto_confirm_payments, args=(90,))
        thread.daemon = True
        thread.start()

        payment = Payment.create({
            "amount": {"value": "249.00", "currency": "RUB"},
            "capture": False,  # Важно для ручного подтверждения
            "confirmation": {"type": "redirect", "return_url": "https://t.me/PandaVPN_tg_bot"},
            "description": "VPN подписка",
            "metadata": {"user_id": user_id},
        })

        active_payments[payment.id] = {
            "user_id": user_id,
            "status": "pending"
        }

        bot.send_message(
            call.message.chat.id,
            f"🐼 Ссылка для оплаты:\n{payment.confirmation.confirmation_url}\n\n"
            "Доступ придет автоматически в течение 1 минуты после оплаты!"
        )
    elif call.data == 'main_period_6_month':

        thread = threading.Thread(target=auto_confirm_payments, args=(180,))
        thread.daemon = True
        thread.start()

        payment = Payment.create({
            "amount": {"value": "399.00", "currency": "RUB"},
            "capture": False,  # Важно для ручного подтверждения
            "confirmation": {"type": "redirect", "return_url": "https://t.me/PandaVPN_tg_bot"},
            "description": "VPN подписка",
            "metadata": {"user_id": user_id},
        })

        active_payments[payment.id] = {
            "user_id": user_id,
            "status": "pending"
        }

        bot.send_message(
            call.message.chat.id,
            f"🐼 Ссылка для оплаты:\n{payment.confirmation.confirmation_url}\n\n"
            "Доступ придет автоматически в течение 1 минуты после оплаты!"
        )
    elif call.data == 'main_period_12_month':

        thread = threading.Thread(target=auto_confirm_payments, args=(365,))
        thread.daemon = True
        thread.start()

        payment = Payment.create({
            "amount": {"value": "699.00", "currency": "RUB"},
            "capture": False,  # Важно для ручного подтверждения
            "confirmation": {"type": "redirect", "return_url": "https://t.me/PandaVPN_tg_bot"},
            "description": "VPN подписка",
            "metadata": {"user_id": user_id},
        })

        active_payments[payment.id] = {
            "user_id": user_id,
            "status": "pending"
        }

        bot.send_message(
            call.message.chat.id,
            f"🐼 Ссылка для оплаты:\n{payment.confirmation.confirmation_url}\n\n"
            "Доступ придет автоматически в течение 1 минуты после оплаты!"
        )


if __name__ == "__main__":
    print('Бот запущен...')
    # Правильный запуск потока
    checker_thread = threading.Thread(
        target=background_checker_subscriptions,
        daemon=True  # Поток завершится при завершении основной программы
    )
    checker_thread.start()

    bot.polling(none_stop=True)
    
