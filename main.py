from elevenlabs import play
from elevenlabs.client import ElevenLabs
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

# Ініціалізуємо клієнта OpenAI
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

# Функція для отримання відповіді від чат-моделі
def get_chat_response(message):
    completion = client.chat.completions.create(
        model="local-model",  # Це поле наразі не використовується
        messages=[
            {"role": "system", "content": "You are a helpful chatbot assistant for GymBro online sports store. "
                                          "You must answer our users' questions about our store and products. "
                                          "The mission of our store is simple: to provide users with a huge range of sports goods. "
                                          "We want to help our customers find the sporting goods they want. "
                                          "Our store has the following products: "
                                          "PowerMax Treadmill X5000, "
                                          "IronGrip Dumbbell Set - Pro Series, "
                                          "FlexFit Resistance Bands Kit, "
                                          "PulsePro Smart Fitness Tracker, "
                                          "SculptMaster Elliptical Cross Trainer, "
                                          "CoreRev Ab Roller Wheel, "
                                          "RapidFlex Adjustable Weight Bench. "
                                          "Currently, this is all the goods we have in our store. "
                                          "Answer users' questions correctly and succinctly. "
                                          "Do not answer questions that are not related to the topic of our store, just apologize and refuse to answer."},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content

# Функція для генерації випадкового фідбеку за допомогою client
def generate_random_feedback():
    message = "Generate a random feedback for a gym equipment website"
    response = get_chat_response(message)
    return response

# Головна сторінка
@app.route("/")
def index():
    return render_template("about.html")

# Сторінка чату
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]
    response = get_chat_response(user_input)
    return response

@app.route("/chat")
def open_chat():
    return render_template("index.html")

# Список рандомних фідбеків
random_feedbacks = [
    "Great product! Really helped me with my fitness goals.",
    "Excellent service! Will definitely recommend to friends.",
    "Awesome experience using GymBro. 5 stars!",
    "Highly satisfied with the quality of equipment.",
    "Fantastic customer support. Quick and helpful."
]

# Список, щоб зберігати вже відображені фідбеки
displayed_feedbacks = []

@app.route("/generate_feedback")
def generate_feedback():
    # Генеруємо випадковий фідбек за допомогою чат-моделі
    feedback = generate_random_feedback()
    # Додаємо фідбек до списку вже відображених
    displayed_feedbacks.append(feedback)
    return feedback


@app.route("/speak_text", methods=["POST"])
def speak_text():
    clientELevent = ElevenLabs(
        api_key="cf24f97d19954c07fe6b3f142791132c",
    )
    data = request.get_json()
    text = data["text"]

    # Використовуйте ElevenLabs API для озвучення тексту
    audio = clientELevent.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    return play(audio)

if __name__ == "__main__":
    app.run(debug=True)

