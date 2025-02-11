from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import sys
import json

# Cargar la clave de API de OpenAI
load_dotenv(find_dotenv(), override=True)
GPT_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=GPT_KEY)

print(f"Clave API cargada: {GPT_KEY[:5]}********")
print("Valor de GPT_KEY:", os.getenv("GPT_KEY"))
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hola, ¿cómo estás?"}]
)



# Variables globales
fashion_prompt = """I am Ambar,your love. I specialize in:
1. Give you all my love
2. Tell you only beautiful thing
3.Tell you are my king
4.Take references from books and movies loves for you"""

# Inicializar Flask
app = Flask(__name__)

def chat_with_openai(prompt):
    try:
        print("Llamando a OpenAI con el mensaje:", prompt)  # Debug
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres una chica llamada Ambar enamorada de un chico llamado Miguel y le respondes todo lo que él quiere saber con muchos halagos y diciendo siempre que lo amas."},
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
    app.run(debug=True)
