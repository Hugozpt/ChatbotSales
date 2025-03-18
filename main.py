
# Base de conocimientos sobre el proceso de admisión
KNOWLEDGE_BASE = {
    "costos": {
        "inscripcion": {
            "primaria": "5,500 MXN",
            "secundaria": "6,000 MXN",
            "bachillerato": "6,500 MXN",
            "bachillerato_tecnologico": "7,000 MXN"
        },
        "colegiatura": {
            "primaria": "3,800 MXN mensuales",
            "secundaria": "4,200 MXN mensuales",
            "bachillerato": "4,500 MXN mensuales",
            "bachillerato_tecnologico": "4,800 MXN mensuales"
        },
        "generales": {
            "examen_admision": "500 MXN",
            "seguro_escolar": "750 MXN anual",
            "credencial": "150 MXN",
            "sociedad_padres": "600 MXN anual"
        }
    }
}

def get_response(query):
    query = query.lower()
    
    if any(word in query for word in ["costo", "precio", "pago", "cuánto", "cuanto"]):
        if "examen" in query:
            return f"El costo del examen de admisión es de {KNOWLEDGE_BASE['costos']['generales']['examen_admision']}"
        elif "inscripción" in query or "inscripcion" in query:
            response = "Costos de inscripción:\n"
            for nivel, costo in KNOWLEDGE_BASE["costos"]["inscripcion"].items():
                response += f"- {nivel.replace('_', ' ').capitalize()}: {costo}\n"
            return response
        else:
            response = "Costos de colegiaturas mensuales:\n"
            for nivel, costo in KNOWLEDGE_BASE["costos"]["colegiatura"].items():
                response += f"- {nivel.replace('_', ' ').capitalize()}: {costo}\n"
            return response
            
    return "Lo siento, no pude entender tu pregunta. Puedes preguntar sobre costos de inscripción, colegiaturas o examen de admisión."

def main():
    print("¡Bienvenido al chatbot del Instituto Carlos Gómez!")
    print("Puedes preguntarme sobre costos de inscripción, colegiaturas y más.")
    print("(Escribe 'salir' para terminar)\n")
    
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == 'salir':
            print("¡Hasta luego!")
            break
            
        response = get_response(user_input)
        print("\nChatbot:", response, "\n")

if __name__ == "__main__":
    main()
