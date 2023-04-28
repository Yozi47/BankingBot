from flask import Flask, request, jsonify
import pickle
import numpy as np
from tensorflow import keras
import json

output_file_path = 'C://Users/zelal/OneDrive/Desktop/ClassFolders/CIS630Project/Dataset2.json'

with open(output_file_path, 'r') as json_file:
    data2 = json.load(json_file)

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

# create a Flask app instance
app = Flask(__name__)

# define a route for handling incoming requests
@app.route('/chatbot', methods=['GET'])
def chatbot():
    # get the input question from the request query string
    question = request.args.get('question')

    # use the model to generate a response
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([question]),
                                         truncating='post', maxlen=max_len))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data2['intents']:
        if i['tag'] == tag:
            response = np.random.choice(i['responses'])

    # return the response in JSON format
    return jsonify({'response': response})

if __name__ == '__main__':
    # run the Flask app
    app.run(debug=True)




# from flask import Flask, request
# from flask_restful import Resource, Api
# import pickle
# import pandas
# import numpy as np
# from flask_cors import CORS
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from sklearn.preprocessing import LabelEncoder
# import json
# import nltk
# import random
#
# app = Flask(__name__)
# api = Api(app)
#
#
# class MyModel(Resource):
#     def get(self, question):
#         # load trained model
#         model = keras.models.load_model('chat_model')
#
#         output_file_path = 'C://Users/zelal/OneDrive/Desktop/ClassFolders/CIS630Project/Dataset2.json'
#         with open(output_file_path, 'r') as json_file:
#             data2 = json.load(json_file)
#         # load tokenizer object
#         with open('tokenizer.pickle', 'rb') as handle:
#             tokenizer = pickle.load(handle)
#
#         # load label encoder object
#         with open('label_encoder.pickle', 'rb') as enc:
#             lbl_encoder = pickle.load(enc)
#
#         # parameters
#         max_len = 20
#
#         def get_response(question):
#             result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([question]),
#                                                                           truncating='post', maxlen=max_len))
#             tag = lbl_encoder.inverse_transform([np.argmax(result)])
#
#             for i in data2['intents']:
#                 if i['tag'] == tag:
#                     response = random.choice(i['responses'])
#                     return response
#
# # data api
#
# #api.add_resource(MyModel, '/api')
# api.add_resource(MyModel, '/chat/<string:question>')
#
# if __name__ == '__main__':
#     app.run(debug=True)