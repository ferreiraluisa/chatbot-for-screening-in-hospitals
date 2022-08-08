import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#https://stackoverflow.com/questions/66092421/how-to-rebuild-tensorflow-with-the-compiler-flags
import numpy as np
import random 
import json
import pickle
import nltk
import joblib
from nltk.stem import WordNetLemmatizer
from tensorflow.python.keras.models import load_model
from medical_record import generate_medical_record


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

symptom_dict = { 1 : "Cough" , 2 : "Muscle aches",  3 : "Tiredness",  4 : "Sore throat",  5 : "Runny nose",  6 : "Stuffy nose",  8 : "Fever ", 9 : "Nause",  10 : "Vomiting", 11 : "Diarrhea", 13 : "Shortness of breath", 14 : " Difficulty in breathing",  15 : " Loss of taste ", 16 : " Loss of smell ", 17 : " Itchy Nose",  18 : " Itchy eyes",  19 : "Itchy inner ear ", 20 : "Sneezing"}

disease_dict = {0 : 'Allergy', 1 : 'Cold', 2 : 'Covid 19', 3 : 'Flu'}

data = {}
data['symptoms'] = []
data['symptom_described'] = []
data['fever_degree'] = []

intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.model')
modelRF = joblib.load('rf_model.sav')
modelKNN = joblib.load('knn_model.sav')

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def clean_up_sentence(sentence):
    setence_words = nltk.word_tokenize(sentence)
    setence_words = [lemmatizer.lemmatize(word) for word in setence_words]
    return setence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])[1]})
    return return_list

def get_response(tag, intents_json, message):
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            if tag == "registration":
                print(result)
                data['name'] = input("")
                print('And how old are you?')
                data['age'] = input("")
                print('What you do for a living?')
                data['job'] = input("")
                print('What is you phone number?')
                data['phone_number'] = input("")
                print("And for how long you are feeling sick?")
                data['days_sick'] = input("")
                print("OK. I create your medical record. Now tell me, how are you feeling?")
            elif tag == "symptoms":
                data['symptom_described'].append(message)
                print(result)
                message = input("")
                symptoms = nltk.word_tokenize(message)
                for symptom in symptoms:
                    if (symptom != ',' or symptom != '.') and symptom.isnumeric():
                        data['symptoms'].append(symptom)
                print("Are you feeling something else?")
            elif tag == "fever":
                data['symptom_described'].append(message)
                print(result)
                degrees = input("")
                degrees = nltk.word_tokenize(degrees)
                for degree in degrees:
                    if isfloat(degree):
                        data["fever_degree"].append(degree)
                print("Are you feeling something else?")
            else:
                print(result)
            break
    return 


print('testando bot....')

tag = "grettings"
while tag != "goodbye":
    message = input("")
    tag = predict_class(message)[0]['intent']
    res = get_response(tag, intents, message)

symptoms = [0] * 20
for i in data['symptoms']:
    symptoms[i-1] = 1

data['rf_model'] = disease_dict.get(modelRF.predict([symptoms])[0])
data['knn_model'] = disease_dict.get(modelKNN.predict([symptoms])[0])

generate_medical_record(data)



