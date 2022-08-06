# traducao_sintomas = { 'tosse' : 'COUGH','dor muscular' : 'MUSCLE_ACHES', 'cansaço' : 'TIREDNESS','dor de garganta' : 'SORE_THROAT','corrimento nasal' : 'RUNNY_NOSE', 'coriza' : 'RUNNY_NOSE' ,'nariz entupido' : 'STUFFY_NOSE', 'febre' : 'FEVER', 'enjoo' : 'NAUSEA','vomito' : 'VOMITING', 'diarreia': 'DIARRHEA','falta de ar' : 'SHORTNESS_OF_BREATH','dificuldade de respirar' : 'DIFFICULTY_BREATHING', 'perca de paladar' : 'LOSS_OF_TASTE','perda de olfato' : 'LOSS_OF_SMELL','nariz coçando':'ITCHY_NOSE','olhos coçando' : 'ITCHY_EYES' , 'boca coçando' : 'ITCHY_MOUTH','ouvido interno coçando' : 'ITCHY_INNER_EAR','espirrando' : 'SNEEZING', 'olho roxo' : 'PINK_EYE'}
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import random 
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Dropout
from tensorflow.python.keras.optimizers import gradient_descent_v2
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?','!','.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)

training = np.array(training, dtype="object")
train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))


opt = gradient_descent_v2.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

model.save('chatbot_model.model', hist)
print("Training complete")
