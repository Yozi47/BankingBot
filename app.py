from flask import Flask
from flask import render_template, request
import pickle
import random
import keras
import numpy as np
import json

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("landingPage.html")
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

# load trained model
model = keras.models.load_model('chat_model')

output_file_path = 'C://Users/zelal/OneDrive/Desktop/ClassFolders/CIS630Project/Dataset2.json'

with open(output_file_path, 'r') as json_file:
    data2 = json.load(json_file)

# load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# parameters
max_len = 20

def chatbot(question):

    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([question]),
                                                                      truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data2['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "Sorry, I don't understand that."


@app.route("/chat", methods=['GET', 'POST'])
def chatbot():
    chats = [] # initialize list of chats
    if request.method == 'POST':
        question = request.form['question']
        response = get_response(question)
        chats.append(Chat(question, 'question'))
        chats.append(Chat(response, 'response'))
    return render_template('chatbot.html', chats=chats)  # pass chats list to template



def get_response(question):
    response = chatbot(question)
    return response
    
class Chat:
    def __init__(self, text, type):
        self.text = text
        self.type = type

if __name__ == "__main__":
    app.run()
