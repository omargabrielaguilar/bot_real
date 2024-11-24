from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Datos del bot
ACCESS_TOKEN = "EAAiKDIVwkusBOZCYRBcAkgZC2mh1oj0q6BGu67XMI8E7ANeZCkITMZA4Iiflyr8AzfUfg74JqQA2lg3onVWGbWuwTZAaLGfBfUZCPKFfodKe4VHZBi86cRioD4N6AHpZB1mhO53y3WwKyj6ZCZC5VaZAqzfgqQaqqwisRTidOEXIEyftA9oNL9tTlHMTW9sNG8WREZAbKepZCjzeW9v8RHWgXpKRg80rvRoy6q6EhQxwZD"  # Tu token
PHONE_NUMBER_ID = "483075861536283"  # ID de tu número de teléfono
WHATSAPP_API_URL = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"

# Define tu token de verificación
VERIFICATION_TOKEN = "nuevo_token_secreto"  # Cambia esto por algo único

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificación del Webhook
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFICATION_TOKEN:
            return challenge, 200
        else:
            return "Verificación fallida", 403

    elif request.method == 'POST':
        # Manejo de mensajes entrantes de WhatsApp
        data = request.get_json()

        if "messages" in data["entry"][0]["changes"][0]["value"]:
            # Extraer el mensaje entrante
            messages = data["entry"][0]["changes"][0]["value"]["messages"]
            for message in messages:
                sender_id = message["from"]  # Número del usuario que envió el mensaje
                text = message["text"]["body"].lower()

                # Lógica del chatbot
                if "hola, requiero información" in text:
                    response = (
                        "Hola, gracias por comunicarte con nosotros. "
                        "Soy un chatbot automático que te ayudará a elegir el mejor producto. "
                        "Puedes elegir las siguientes opciones:\n"
                        "- Servicios\n"
                        "- Productos\n"
                        "- Dirección"
                    )
                elif text == "servicios":
                    response = (
                        "En REAL COMPUTER S.A.C. contamos con los siguientes servicios:\n"
                        "- Reparación de Equipos Informáticos\n"
                        "- Servicio CCTV\n\n"
                        "¿Te podemos ayudar en alguna otra consulta? (si/no)"
                    )
                elif text == "productos":
                    response = (
                        "En REAL COMPUTER S.A.C. contamos con el siguiente catálogo de productos:\n"
                        "- Producto A\n"
                        "- Producto B\n\n"
                        "¿Te podemos ayudar en alguna otra consulta? (si/no)"
                    )
                elif text == "dirección":
                    response = (
                        "Calle Tres #503 Bs As\n\n"
                        "¿Te podemos ayudar en alguna otra consulta? (si/no)"
                    )
                elif text == "si":
                    response = "Estaremos aquí en 2 minutos. ¡Gracias por tu paciencia! Fin."
                elif text == "no":
                    response = "Gracias por contactarnos. Fin."
                else:
                    response = (
                        "Lo siento, no entendí tu mensaje. "
                        "Por favor, elige una opción válida:\n"
                        "- Servicios\n"
                        "- Productos\n"
                        "- Dirección"
                    )

                # Enviar la respuesta al usuario
                send_whatsapp_message(sender_id, response)

        return jsonify({"status": "success"}), 200


def send_whatsapp_message(recipient_id, message):
    """Envía un mensaje usando la API de WhatsApp"""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,  # Número dinámico que envió el mensaje
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    print(response.status_code, response.json())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
