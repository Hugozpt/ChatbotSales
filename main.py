from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Base de conocimientos sobre el proceso de admisión
KNOWLEDGE_BASE = {
    "costos": {
        "inscripcion": {
            "primaria": "6,900 MXN",
            "secundaria": "7,400 MXN",
            "bachillerato": "7,900 MXN",
            "bachillerato_tecnologico": "8,000 MXN"
        },
        "colegiatura": {
            "primaria": "4,100 MXN mensuales",
            "secundaria": "4,600 MXN mensuales",
            "bachillerato": "4,900 MXN mensuales",
            "bachillerato_tecnologico": "4,900 MXN mensuales"
        },
        "generales": {
            "examen_admision": "500 MXN",
            "seguro_escolar": "750 MXN anual",
            "credencial": "150 MXN",
            "sociedad_padres": "1000 MXN anual"
        }
    },
    "respuestas": {
        "inscripcion": {
            "general": "La inscripción incluye los materiales básicos del ciclo escolar, seguro contra accidentes y credencial escolar.",
            "primaria": "La inscripción en primaria cuesta 6,900 MXN e incluye los libros de texto básicos.",
            "secundaria": "La inscripción en secundaria tiene un costo de 7,400 MXN e incluye el material didáctico inicial.",
            "bachillerato": "Para bachillerato, la inscripción cuesta 7,900 MXN e incluye la guía de estudio.",
            "bachillerato_tecnologico": "El bachillerato tecnológico tiene una inscripción de 7,900 MXN que incluye acceso a laboratorios especializados."
        },
        "colegiatura": {
            "general": "Las colegiaturas se pagan mensualmente durante 10 meses (septiembre a junio) y cubren todas las clases regulares.",
            "primaria": "La colegiatura mensual de primaria es de 4,100 MXN e incluye actividades deportivas básicas.",
            "secundaria": "En secundaria, la colegiatura de 4,600 MXN mensuales incluye talleres complementarios.",
            "bachillerato": "La colegiatura de bachillerato es 4,900 MXN al mes e incluye orientación vocacional.",
            "bachillerato_tecnologico": "El bachillerato tecnológico tiene una colegiatura de 4,900 MXN mensuales que incluye prácticas en talleres."
        },
        "examen": {
            "general": "El examen de admisión tiene un costo de 500 MXN y evalúa conocimientos básicos según el nivel.",
            "fechas": "Los exámenes se realizan en fechas específicas que pueden consultarse en la página web oficial.",
            "requisitos": "Para presentar el examen se requiere identificación y comprobante de pago."
        }
    }
}

def preprocess_query(query):
    tokens = word_tokenize(query.lower())
    stop_words = set(stopwords.words('spanish'))
    return [token for token in tokens if token not in stop_words]

def get_response(query):
    processed_query = preprocess_query(query)
    query = ' '.join(processed_query)

    # Only respond with greeting if it's just a greeting
    greetings = ["hola", "buenos días", "buenos dias", "buenas tardes", "buenas noches", "saludos", "qué tal", "que tal", "hi", "hello"]
    if query in greetings or query.strip() in greetings:
        return "¡Hola! Soy el asistente virtual del Instituto Carlos Gómez. ¿En qué puedo ayudarte?"

    if any(word in query for word in ["costo", "precio", "pago", "cuánto", "cuanto", "vale", "cobran", "cuesta", "inscripcion", "inscripción"]):
        if any(word in query for word in ["examen", "prueba", "admision", "admisión"]):
            response = KNOWLEDGE_BASE["respuestas"]["examen"]["general"] + "\n"
            response += f"Costo: {KNOWLEDGE_BASE['costos']['generales']['examen_admision']}\n"
            response += KNOWLEDGE_BASE["respuestas"]["examen"]["fechas"]
            return response

        elif any(word in query for word in ["inscripción", "inscripcion", "inscribir"]):
            if "primaria" in query:
                return KNOWLEDGE_BASE["respuestas"]["inscripcion"]["primaria"]
            elif "secundaria" in query:
                return KNOWLEDGE_BASE["respuestas"]["inscripcion"]["secundaria"]
            elif any(word in query for word in ["tecnologico", "técnico"]):
                return KNOWLEDGE_BASE["respuestas"]["inscripcion"]["bachillerato_tecnologico"]
            elif any(word in query for word in ["bachillerato", "prepa"]):
                return KNOWLEDGE_BASE["respuestas"]["inscripcion"]["bachillerato"]
            else:
                response = KNOWLEDGE_BASE["respuestas"]["inscripcion"]["general"] + "\n\nCostos de inscripción:\n"
                for nivel, costo in KNOWLEDGE_BASE["costos"]["inscripcion"].items():
                    response += f"- {nivel.replace('_', ' ').capitalize()}: {costo}\n"
                return response

        elif any(word in query for word in ["colegiatura", "mensualidad", "mes"]):
            if "primaria" in query:
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["primaria"]
            elif "secundaria" in query:
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["secundaria"]
            elif "tecnologico" in query or "técnico" in query:
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["bachillerato_tecnologico"]
            elif "bachillerato" in query or "prepa" in query:
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["bachillerato"]
            else:
                response = KNOWLEDGE_BASE["respuestas"]["colegiatura"]["general"] + "\n\nColegiaturas mensuales:\n"
                for nivel, costo in KNOWLEDGE_BASE["costos"]["colegiatura"].items():
                    response += f"- {nivel.replace('_', ' ').capitalize()}: {costo}\n"
                return response

    if any(word in query for word in ["padres", "familia", "sociedad", "cuota", "asociacion"]):
        return f"La cuota anual de la Sociedad de Padres de Familia es de {KNOWLEDGE_BASE['costos']['generales']['sociedad_padres']} para todas las secciones del Instituto."

    return "Lo siento, no pude entender tu pregunta. Puedes preguntar sobre costos de inscripción, colegiaturas, examen de admisión o cuotas de padres de familia."


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message', '')
    response = get_response(query)
    return jsonify({'response': response})

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot Instituto Carlos Gómez</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
            #chat-box { height: 400px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
            #input-box { width: 80%; padding: 5px; }
            button { padding: 5px 15px; }
        </style>
    </head>
    <body>
        <h1>Chatbot Instituto Carlos Gómez</h1>
        <div id="chat-box"></div>
        <input type="text" id="input-box" placeholder="Escribe tu pregunta aquí...">
        <button onclick="sendMessage()">Enviar</button>
        <script>
            function sendMessage() {
                const input = document.getElementById('input-box');
                const chatBox = document.getElementById('chat-box');
                const message = input.value;

                if (!message) return;

                chatBox.innerHTML += `<p><strong>Tú:</strong> ${message}</p>`;
                input.value = '';

                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    chatBox.innerHTML += `<p><strong>Chatbot:</strong> ${data.response}</p>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                });
            }

            document.getElementById('input-box').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)