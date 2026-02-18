import os
import telebot
import google.generativeai as genai

# Usamos los nombres exactos que configuramos en Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN') 
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Configuración de IA
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ACTIVACIÓN DEL BOT (Sin hilos para evitar el Error 409)
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error Gemini: {e}")

if __name__ == "__main__":
    print(">>> ArantzaBot2 iniciando conexión única...")
    bot.infinity_polling()
