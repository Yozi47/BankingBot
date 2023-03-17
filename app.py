from flask import Flask
from flask import render_template, request
app = Flask(__name__)

@app.route("/")
@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/signup.html")
def signup():
    return render_template("signup.html")


@app.route("/home.html")
def home():
    return render_template("home.html")

@app.route("/eServ.html")
def eserv():
    return render_template("eServ.html")

@app.route("/acc.html")
def acc():
    return render_template("acc.html")


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/aboutUs.html")
def about():
    return render_template("aboutUs.html")


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
    
class Chat:
    def __init__(self, text, type):
        self.text = text
        self.type = type
