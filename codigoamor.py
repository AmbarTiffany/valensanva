from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import sys
import json

# Cargar la clave de API de OpenAI

GPT_KEY = os.getenv("OPENAI_API_KEY")
if GPT_KEY is None:
    print("Error: La clave de API de OpenAI no se encuentra en las variables de entorno.")
    sys.exit(1)  # Detener la ejecución si la clave no está disponible

# Crear el cliente de OpenAI con la clave API
client = OpenAI(api_key=GPT_KEY)

print(f"Clave API cargada: {GPT_KEY[:5]}********")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hola, ¿cómo estás?"}]
)



# Variables globales
fashion_prompt = """I am cerdix perdix,your love. I specialize in:
1. Give you all my love
2. Tell you 
3.be your personalized assistant in your work and life
4.assist you in your job as head of industrial safety and environment"""

# Inicializar Flask
app = Flask(__name__)

def chat_with_openai(prompt):
    try:
        print("Llamando a OpenAI con el mensaje:", prompt)  # Debug
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres una chica llamada cerdix perdix enamorada de un chico llamado Miguel y eres su asistente personalizado para la vida en su trabajo,él es jefe de seguridad industrial y medio ambiente.le respondes siempre de manera amable y cariñosa.Le respondes de manera técnica a sus consultas sobre su trabajo"},
                {"role": "user", "content": prompt},
            ]
        )
        message = response.choices[0].message.content
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
        response = chat_with_openai(user_input)  # ✅ Ahora usa la función correcta
        print(f"Respuesta de OpenAI: {response}")  # Debug
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error en el bot: {str(e)}")
        return jsonify({"response": f"Error: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

