import telebot
from forex_python.converter import CurrencyRates

TOKEN = '6950960593:AAH5VjV_mUCyUgjPkVamBRBpmIzwL3dI3cw'

bot = telebot.TeleBot(TOKEN)
c = CurrencyRates()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для конвертации валют. Выбери валюту, из которой будем конвертировать:")
    send_initial_currency_keyboard(message)

def send_initial_currency_keyboard(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons = [telebot.types.KeyboardButton(currency) for currency in c.get_rates('USD')]
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Выбери валюту, из которой будем конвертировать:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_selected_initial_currency)

def handle_selected_initial_currency(message):
    selected_currency = message.text
    send_target_currency_keyboard(message, selected_currency)

def send_target_currency_keyboard(message, selected_currency):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons = [telebot.types.KeyboardButton(currency) for currency in c.get_rates('USD') if currency != selected_currency]
    markup.add(*buttons)

    bot.send_message(message.chat.id, "Выбери валюту, в которую будем конвертировать:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_selected_target_currency, selected_currency)

def handle_selected_target_currency(message, selected_currency):
    target_currency = message.text
    bot.send_message(message.chat.id, "Теперь введите сумму для конвертации:")
    bot.register_next_step_handler(message, handle_conversion_amount, selected_currency, target_currency)

def handle_conversion_amount(message, selected_currency, target_currency):
    try:
        amount = float(message.text)
        result = c.convert(selected_currency, target_currency, amount)
        bot.send_message(message.chat.id, f"{amount:.2f} {selected_currency} = {result:.2f} {target_currency}")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число для конвертации.")

if __name__ == '__main__':
    bot.polling(none_stop=True)