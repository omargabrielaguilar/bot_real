from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Página inicial con mensaje de bienvenida"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """API para manejar los mensajes del chatbot"""
    user_message = request.json.get('message', '').lower()

    # Respuesta inicial
    if "información" in user_message:
        bot_response = (
            "Hola, gracias por comunicarte con nosotros. "
            "Soy un chatbot automático que te ayudará a elegir el mejor producto. "
            "Puedes elegir las siguientes opciones:\n"
            "- Servicios\n"
            "- Productos\n"
            "- Dirección"
        )
    else:
        bot_response = "Lo siento, no entendí tu mensaje. Por favor, escribe 'información' para empezar."

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
