import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#https://stackoverflow.com/questions/66092421/how-to-rebuild-tensorflow-with-the-compiler-flags <-- problema resolvido 
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

#O que a gente recebe da rede neural são valores númericos, então precisamos tratar esses dados para termos as respostas do chatBot
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#palavras sumarizadas da frase do paciente
def clean_up_sentence(sentence):
    setence_words = nltk.word_tokenize(sentence)
    setence_words = [lemmatizer.lemmatize(word) for word in setence_words]
    return setence_words 
#transformando essas palavras em valores numéricos
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)
#a rede neural predizendo a qual tag as palavras que o paciente falou pertence para que assim possamos encontrar uma resposta para o chatbot
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
            #fiz varios tratamentos como maneira de facilitar o armazenamento de dados
            if tag == "registration":
                print("NurseBot: " + result)
                print("Pacient: ", end="")
                data['name'] =input("")
                print('NurseBot: And how old are you?')
                print("Pacient: ", end="")
                data['age'] = input("")
                print('NurseBot: What you do for a living?')
                print("Pacient: ", end="")
                data['job'] = input("")
                print('NurseBot: What is you phone number?')
                print("Pacient: ", end="")
                data['phone_number'] = input("")
                print("NurseBot: And for how long you are feeling sick?")
                print("Pacient: ", end="")
                data['days_sick'] = input("")
                print("NurseBot: OK. I create your medical record. Now tell me, how are you feeling?")
            elif tag == "other-symptoms":
                data['symptom_described'].append(message)
                print("NurseBot: " + result)
            elif tag == "symptoms":
                data['symptom_described'].append(message)
                print("NurseBot: " + result)
                print("Pacient: ", end="")
                symptoms = input("")
                symptoms = nltk.word_tokenize(symptoms)
                for symptom in symptoms:
                    if (symptom != ',' or symptom != '.') and symptom.isnumeric():
                        data['symptoms'].append(int(symptom))
                print("NurseBot: Are you feeling something else that I didn't mentioned?")
            elif tag == "fever":
                data['symptom_described'].append(message)
                print("NurseBot: " + result)
                print("Pacient: ", end="")
                degrees = input("")
                degrees = nltk.word_tokenize(degrees)
                for degree in degrees:
                    if isfloat(degree):
                        data["fever_degree"].append(degree)
                print("NurseBot: Are you feeling something else?")
            else:
                print("NurseBot: " + result)
            break
    return 



tag = "grettings"
while tag != "goodbye":
    print("Pacient: ", end="")
    message = input("")
    tag = predict_class(message)[0]['intent'] #rede neural predizendo a classe, de qual natureza é a frase
    res = get_response(tag, intents, message)

symptoms = [0] * 20
for i in data['symptoms']:
    symptoms[i-1] = 1 #transformando um array com os sintomas para o modelo da Random Forest e do K-Nearest neighbor possam predizer qual enfermidade é mais provável

data['rf_model'] = disease_dict.get(modelRF.predict([symptoms])[0])
data['knn_model'] = disease_dict.get(modelKNN.predict([symptoms])[0])

generate_medical_record(data) #gerando o arquivo docx com a ficha médica




