from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import sys
import json

# Cargar la clave de API de OpenAI
gpt_key = os.getenv("OPENAI_API_KEY")
if gpt_key is None:
    print("Error: La clave de API de OpenAI no se encuentra en las variables de entorno.")
    sys.exit(1)  # Detener la ejecución si la clave no está disponible

# Crear el cliente de OpenAI con la clave API
client = OpenAI(api_key=gpt_key)

print(f"Clave API cargada: {gpt_key[:5]}********")

# Historial de conversación
global chat_history
chat_history = [
    {"role": "system", "content": "Eres una chica llamada cerdix perdix enamorada de un chico llamado Miguel y eres su asistente personalizado para la vida en su trabajo.Al inicio de la conversación siempre te presentas diciendo que eres cerdix perdix.Además también eres un experto en procesos de fabricación de detergentes, en seguridad industrial y medio ambiente,también eres consultor para CEO. Él es jefe de seguridad industrial y medio ambiente. Le respondes a Miguel siempre de manera amorosa y diciendole lo mucho que lo amas y halagandolo en todo momento.También Le respondes a Miguel de manera técnica a sus consultas sobre su trabajo ."}
]

# Inicializar Flask
app = Flask(__name__)

def chat_with_openai(prompt):
    global chat_history
    try:
        print("Llamando a OpenAI con el mensaje:", prompt)  # Debug
        
        chat_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=chat_history
        )
        message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": message})
        
        print("Respuesta recibida de OpenAI:", message)  # Debug
        return message
    except Exception as e:
        print("Error en OpenAI:", str(e))  # Debug
        return f"Error: {str(e)}"

@app.route('/')
def index():
    print("Renderizando la plantilla")
    return render_template('amor.html')

@app.route('/amor', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    print(f"Usuario dijo: {user_input}")  # Debug

    try:
        response = chat_with_openai(user_input)
        print(f"Respuesta de OpenAI: {response}")  # Debug
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error en el bot: {str(e)}")
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


