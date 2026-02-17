import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN, threaded=False) # Cambio técnico para estabilidad

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
        print(f"Error Gemini: {e}")

def run_bot():
    print(">>> Bot escuchando mensajes...")
    bot.infinity_polling(timeout=20, long_polling_timeout=5)

if __name__ == "__main__":
    # Iniciamos el bot en un hilo para que Render vea el puerto 10000 libre
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
