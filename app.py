from flask import Flask
from flask import render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("bot_layout.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


@app.route("/chat", methods=['GET', 'POST'])
def chatbot():
    chats = [] # initialize list of chats
    if request.method == 'POST':
        question = request.form['question']
        response = get_response(question)
        chats.append(Chat(question, 'question'))
        chats.append(Chat(response, 'response'))
    return render_template('chatbot.html', chats=chats) # pass chats list to template


def get_response(question):
    responses = {
        'What is your name?': 'My name is Chatbot',
        'What is the weather like today?': 'I am sorry, I am not programmed to provide weather forecasts',
        'What time is it?': 'I am sorry, I am not programmed to provide time information',
        'How are you?': 'I am doing well, thank you for asking!'
    }
    # Retrieve the response from the dictionary
    if question in responses:
        return responses[question]
    else:
        return 'I am sorry, I do not understand your question'