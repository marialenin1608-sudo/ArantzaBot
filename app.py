import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# Carga de credenciales desde las variables de entorno de Render
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# Configuración de Gemini 1.5 Flash (Gratis y rápido)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN)

# Servidor Flask para mantener vivo el servicio en Render
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot de Xyon Group activo y funcionando", 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Generar respuesta con la IA de Google
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error en el procesamiento: {e}")

def run_bot():
    print("Iniciando conexión con Telegram...")
    # El polling infinito mantiene al bot escuchando mensajes
    bot.infinity_polling()

if __name__ == "__main__":
    # Ejecutamos el bot en un hilo separado para que no bloquee a Flask
    threading.Thread(target=run_bot).start()
    
    # Render asigna un puerto dinámico mediante la variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
