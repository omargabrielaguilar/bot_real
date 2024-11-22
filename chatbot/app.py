from flask import Flask, request, jsonify
import pyautogui
import time
import webbrowser

app = Flask(__name__)

BOT_NUMBER = "+51901856517"  # Número fijo del bot

def send_whatsapp_message(message):
    """Envía un mensaje de WhatsApp usando pyautogui"""
    # Abre WhatsApp Web con el número del bot
    webbrowser.open(f"https://wa.me/{BOT_NUMBER}")
    time.sleep(5)  # Espera a que la página cargue

    # Escribe el mensaje
    pyautogui.typewrite(message)
    time.sleep(1)

    # Presiona "Enter" para enviar el mensaje
    pyautogui.press("enter")

@app.route('/send-message', methods=['POST'])
def send_message():
    """Endpoint para enviar mensajes manualmente"""
    # Obtener el mensaje del cuerpo de la solicitud
    data = request.json
    user_message = data.get("message", "").lower()

    # Respuesta inicial: usuario pide información
    if "hola, requiero información" in user_message:
        bot_response = (
            "Hola, gracias por comunicarte con nosotros. "
            "Soy un chatbot automático que te ayudará a elegir el mejor producto. "
            "Puedes elegir las siguientes opciones:\n"
            "- Servicios\n"
            "- Productos\n"
            "- Dirección"
        )
    elif user_message == "servicios":
        bot_response = (
            "En REAL COMPUTER S.A.C. contamos con los siguientes servicios:\n"
            "- Reparación de Equipos Informáticos\n"
            "- Servicio CCTV\n\n"
            "¿Te podemos ayudar en alguna otra consulta? (si/no)"
        )
    elif user_message == "productos":
        bot_response = (
            "En REAL COMPUTER S.A.C. contamos con el siguiente catálogo de productos:\n"
            "- Producto A\n"
            "- Producto B\n\n"
            "¿Te podemos ayudar en alguna otra consulta? (si/no)"
        )
    elif user_message == "dirección":
        bot_response = (
            "Calle Tres #503 Bs As\n\n"
            "¿Te podemos ayudar en alguna otra consulta? (si/no)"
        )
    elif user_message == "si":
        bot_response = "Estaremos aquí en 2 minutos. ¡Gracias por tu paciencia! Fin."
    elif user_message == "no":
        bot_response = "Gracias por contactarnos. Fin."
    else:
        bot_response = (
            "Lo siento, no entendí tu mensaje. "
            "Por favor, elige una opción válida:\n"
            "- Servicios\n"
            "- Productos\n"
            "- Dirección"
        )

    # Enviar el mensaje usando pyautogui
    send_whatsapp_message(bot_response)

    # Respuesta para monitoreo
    return jsonify({"status": "message sent", "response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
