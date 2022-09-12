import requests

BOT_KEY = '5653183590:AAEKjieJ4dVWERCAwvMpBX3F0b2sRBlJa3U'

def get_weather(city):
    API_KEY = '485927224f21ab004283eefa2e85eabe'
    response_API = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}')
    temp = round(response_API.json()['main']['temp'])
    city = response_API.json()['name']
    return f'City: {city}\nTemperature: {temp}°C'



import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter city name to get weather forecast")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_weather(update.message.text))


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Weather',
            input_message_content=InputTextMessageContent(get_weather(query.upper()))
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)



if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_KEY).build()

    start_handler = CommandHandler('start', start)
    inline_handler = InlineQueryHandler(inline_caps)
    echo_handler = MessageHandler(filters.TEXT, echo)

    application.add_handler(start_handler)
    application.add_handler(inline_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()
