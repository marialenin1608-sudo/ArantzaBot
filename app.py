import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. Configuración de credenciales (Nombres exactos de Render)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN') 
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# 2. Inicialización
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)

# 3. Servidor Web para que Render esté feliz
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot de Xyon Group activo", 200

# 4. Lógica del Bot
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error Gemini: {e}")

def run_bot():
    print(">>> Bot escuchando mensajes...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Arrancar el bot en un hilo separado
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    # Arrancar Flask en el puerto que Render exige
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
