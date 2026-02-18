import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. Definimos las variables usando el nombre que está en Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN') 
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# 2. Configuramos Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Configuramos el Bot usando EXACTAMENTE la misma variable
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot de Xyon Group activo", 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")

def run_bot():
    print(">>> Bot escuchando mensajes...")
    bot.infinity_polling(timeout=20, long_polling_timeout=5)

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
