from flask import Flask, render_template, request
import json 
import numpy as np
from tensorflow import keras
# from sklearn.preprocessing import LabelEncoder
import pickle

app = Flask(__name__)

# load trained model
model = keras.models.load_model('chat_model')

# load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# parameters
max_len = 20

# load intents from JSON file
with open(output_file_path, 'r') as json_file:
    data = json.load(json_file)

# chat function
def chat(inp):
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
    label_index = np.argmax(result)

    for i in data['intents']:
        if i['tag'] == label_index:
            return random.choice(i['responses'])

# home page
@app.route("/")
def home():
    return render_template("index.html")

# chatbot API
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.form["user_message"]
    bot_response = chat(user_message)
    return {"bot_response": bot_response}

if __name__ == "__main__":
    app.run(debug=True)
