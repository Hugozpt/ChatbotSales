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
            "primaria": "8,970 MXN",
            "secundaria": "9,970 MXN",
            "bachillerato_universitario": "12,390 MXN",
            "bachillerato_tecnologico": "10,710 MXN"
        },
        "colegiatura": {
            "primaria": "3,220 MXN mensuales",
            "secundaria": "3,550 MXN mensuales",
            "bachillerato_universitario": "4,270 MXN mensuales",
            "bachillerato_tecnologico": "4,270 MXN mensuales"
        },
        "generales": {
            "examen_admision": "350 MXN",
            "seguro_escolar": "750 MXN anual",
            "credencial": "150 MXN",
            "sociedad_padres": "1000 MXN anual"
        }
    },
    "respuestas": {
        "inscripcion": {
            "general": "La inscripción es de pago por anualidad.",
            "primaria": "La inscripción en primaria cuesta 8,970 MXN e incluye los libros de texto básicos.",
            "secundaria": "La inscripción en secundaria tiene un costo de 9,970 MXN e incluye el material didáctico inicial.",
            "bachillerato_universitario": "Para bachillerato, la inscripción cuesta 12,390 MXN e incluye la guía de estudio.",
            "bachillerato_tecnologico": "El bachillerato tecnológico tiene una inscripción de 10,710 MXN que incluye acceso a laboratorios especializados."
        },
        "colegiatura": {
            "general": "Las colegiaturas se pagan mensualmente durante 10 meses y cubren todas las clases regulares.",
            "primaria": "La colegiatura mensual de primaria es de 3,220 MXN e incluye actividades deportivas básicas.",
            "secundaria": "En secundaria, la colegiatura de 3,550 MXN mensuales incluye talleres complementarios.",
            "bachillerato_univesitario": "La colegiatura de bachillerato es 4,270 MXN al mes e incluye orientación vocacional.",
            "bachillerato_tecnologico": "El bachillerato tecnológico tiene una colegiatura de 4,270 MXN mensuales que incluye prácticas en talleres."
        },
        "examen": {
            "general": "El examen de admisión tiene un costo de 350 MXN y evalúa conocimientos básicos según el nivel.",
            "fechas": "Los exámenes se realizan en fechas específicas como Primaria-Secundaria-Bachillerato Universitario. 1° Sábado 7 de Diciembre 2024, 2° Sábado 08 de Febrero 2025 y 3° Sábado 15 de Marzo 2025. Y Bachillerato Tecnológico 1° Sábado 14 de Diciembre 2024, 2° Sábado 01 de Febrero 2025 y 3° Sábado 01 de Marzo 2025 y 4° Sábado 05 de Abril 2025.",
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

    if any(word in query for word in ["costo", "precio", "pago", "cuánto", "cuanto", "vale", "cobran", "cuesta", "inscripcion", "inscripción", "inscribir", "colegiatura", "mensualidad", "mes"]):
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
            elif any(word in query for word in ["tecnologico", "tecnológico", "bachillerato tecnológico"]):
                return KNOWLEDGE_BASE["respuestas"]["inscripcion"]["bachillerato_tecnologico"]
            elif any(word in query for word in ["universitario", "bachillerato universitario", "prepa"]):
                return KNOWLEDGE_BASE["respuestas"]["inscripcion"]["bachillerato_universitario"]
            else:
                response = KNOWLEDGE_BASE["respuestas"]["inscripcion"]["general"] + "\n\nCostos de inscripción:\n"
                for nivel, costo in KNOWLEDGE_BASE["costos"]["inscripcion"].items():
                    response += f"- {nivel.replace('_', ' ').capitalize()}: {costo}\n"
                return response

        elif any(word in query for word in ["colegiatura", "mensualidad", "mes"]):
            # Check for specific section
            if "primaria" in query:
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["primaria"]
            elif "secundaria" in query:
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["secundaria"]
            elif any(word in query for word in ["tecnologico", "tecnológico", "bachillerato tecnológico"]):
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["bachillerato_tecnologico"]
            elif any(word in query for word in ["universitario", "bachillerato universitario", "prepa"]):
                return KNOWLEDGE_BASE["respuestas"]["colegiatura"]["bachillerato_univesitario"]
            else:
                # General response for all sections
                response = KNOWLEDGE_BASE["respuestas"]["colegiatura"]["general"] + "\n\nColegiaturas mensuales:\n"
                for nivel, costo in KNOWLEDGE_BASE["costos"]["colegiatura"].items():
                    response += f"- {nivel.replace('_', ' ').capitalize()}: {costo}\n"
                return response

    # New block for admission exams
    if any(word in query for word in ["examen", "prueba", "admision", "admisión"]):
        response = KNOWLEDGE_BASE["respuestas"]["examen"]["general"] + "\n"
        response += f"Costo: {KNOWLEDGE_BASE['costos']['generales']['examen_admision']}\n"
        response += KNOWLEDGE_BASE["respuestas"]["examen"]["fechas"] + "\n"
        response += KNOWLEDGE_BASE["respuestas"]["examen"]["requisitos"]
        return response

    # New block for contact information
    if any(word in query for word in ["contacto", "teléfono", "telefono", "número", "email", "correo"]):
        return (
            "Puedes ponerte en contacto con nosotros a través de los siguientes medios:\n"
            "- Correo electrónico: comunicacion@salesianoicg.edu.mx\n"
            "- Correo electrónico Bachillerato Tecnológico: oficinabtec@tecnologico-cg.edu.mx\n"
            "- Oficinas: 444 813 3668\n"
            "- Promociones y Admisiones:  444-813-0978\n"
            "- Admisiones Bachillerato Tecnológico: 444 714 8089\n"
        )

    if any(word in query for word in ["padres", "familia", "sociedad", "cuota", "asociacion"]):
        return f"La cuota anual de la Sociedad de Padres de Familia es de {KNOWLEDGE_BASE['costos']['generales']['sociedad_padres']} para todas las secciones del Instituto."

    return "Lo siento, no pude entender tu pregunta. Puedes preguntar sobre costos de inscripción, colegiaturas, examen de admisión, cuotas de padres de familia o información de contacto."


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
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                background-color: #f9f9f9;
            }
            .chat-icon {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 60px;
                height: 60px;
                background-color: #007bff;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .chat-icon img {
                width: 30px;
                height: 30px;
            }
            .chat-window {
                position: fixed;
                bottom: 80px;
                right: 20px;
                width: 300px;
                height: 400px;
                background-color: #ffffff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                display: none;
                flex-direction: column;
                overflow: hidden;
            }
            .chat-header {
                background-color: #007bff;
                color: white;
                padding: 10px;
                text-align: center;
                font-size: 1.2rem;
            }
            .chat-body {
                flex: 1;
                padding: 10px;
                overflow-y: auto;
                background-color: #f9f9f9;
            }
            .chat-body p {
                margin: 5px 0;
            }
            .chat-body .user {
                text-align: right;
                color: #007bff;
            }
            .chat-body .bot {
                text-align: left;
                color: #333;
            }
            .chat-footer {
                display: flex;
                padding: 10px;
                background-color: #ffffff;
                border-top: 1px solid #ccc;
            }
            .chat-footer input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-right: 10px;
            }
            .chat-footer button {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .chat-footer button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="chat-icon" onclick="toggleChat()">
            <img src="https://cdn-icons-png.flaticon.com/512/134/134914.png" alt="Chat Icon">
        </div>
        <div class="chat-window" id="chat-window">
            <div class="chat-header">Chatbot</div>
            <div class="chat-body" id="chat-body">
                <p class="bot"><strong>Chatbot:</strong> ¡Hola! Soy el asistente virtual del Instituto Carlos Gómez. ¿En qué puedo ayudarte?</p>
            </div>
            <div class="chat-footer">
                <input type="text" id="chat-input" placeholder="Escribe tu mensaje...">
                <button onclick="sendMessage()">Enviar</button>
            </div>
        </div>
        <script>
            function toggleChat() {
                const chatWindow = document.getElementById('chat-window');
                chatWindow.style.display = chatWindow.style.display === 'none' || chatWindow.style.display === '' ? 'flex' : 'none';
            }

            function sendMessage() {
                const input = document.getElementById('chat-input');
                const chatBody = document.getElementById('chat-body');
                const message = input.value;

                if (!message) return;

                // Add user message to chat
                chatBody.innerHTML += `<p class="user"><strong>Tú:</strong> ${message}</p>`;
                input.value = '';

                // Send message to server
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    // Add bot response to chat
                    chatBody.innerHTML += `<p class="bot"><strong>Chatbot:</strong> ${data.response}</p>`;
                    chatBody.scrollTop = chatBody.scrollHeight;
                });
            }

            document.getElementById('chat-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)