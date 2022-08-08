<a>
    <img src="https://cdn.discordapp.com/attachments/729689711416967239/844210892916523018/Ygemzly2XsP3gzFbXjFyExvD00B3rBvPbDEOoNOB-4uL4NLF1YKM6kiypik1H4koNc5_sNVAAAy_PDq_kmh_CRmn1dvC1uyeckCs.png" alt="UFV logo" title="UFV" align="right" height="55" />
</a>
<br>
<h1 align = "center"> Trabalho Final - INF420 </h1>


<h2 align = "center"> ChatBot para triagem em Hospitais </h2>


## Índice

- [Resumo](#Resumo)
- [Introdução](#Introdução)
- [Metodologia](#Metodologia)
- [Resultados](#Resultados)
- [Conclusão](#Conclusão)
- [Referências](#Referências)
- [Responsáveis](#Responsáveis)

## Resumo
&emsp;&emsp;Projeto final apresentado à disciplina de Inteligência Artificial I, de código INF 420, ministrada pelo professor Julio C. S. Reis, como requisito parcial para aprovação na disciplina.

## Introdução
&emsp;&emsp;O trabalho proposto é um chatbot responsável por fazer triagem em hospitais para diferenciar os casos de COVID entre os seguintes casos com sintomas semelhantes: alergia, resfriado e gripe. Além disso, no final, ele gera uma ficha médica do paciente com informações pessoais, como nome, idade, profissão, os sintomas, quantos dias ele está doente e resultado da predição feito com técnicas de inteligência artificial. 
&emsp;&emsp;Para conseguir usar o chatBot, é necessário rodar randomforest_knn.py e trainingBot.py antes de rodar o chatBot.py.
 
## Metodologia
&emsp;&emsp;Utilizei um <a href="https://www.kaggle.com/datasets/walterconway/covid-flu-cold-symptoms">dataset</a> disponível no Kaggle, com vários casos de enfermidade junto aos seus sintomas e a classificação de cada um dos casos como alergia, resfriado, covid ou gripe. Essa base de dados está desbalanceada, existem muitos casos de alergia e gripe em comparação com covid e resfriado,isso é um problema pois pode gerar muitos "alarmes falsos", o diagnóstico acabaria tendenciando muito para alergia e gripe, pois tem muitas amostras e por os sintomas entre as quatro enfermidades serem bem semelhantes, além de dificultar a avaliação de eficácia. Por isso, utilizei a técnica de under-sampling, com o método RandomUnderSampler() da biblioteca imblearn.under_sampling.<br>
    <figure align="left">
        <img src="imagens/without_under_sampling.png" alt="sem under sampling" height= "250">
        <figcaption>Sem under sampling</figcaption>
    </figure>
    <figure align="right" >
        <img src="imagens/with_under_sampling.png" alt="sem under sampling"  height= "250">
        <figcaption>Com under sampling</figcaption>
    </figure>
<br>
&emsp;&emsp;Para resolver o problema de classificação, utilizei duas técnicas: Random Forest e K-Nearest neighbor. Para random forest, coloquei o número de árvores de decisão como 10, com critério entropy de separação e um random_state de 42. Para o K-Nearest neighbor, coloquei um número de vizinhos de 10 e a métrica euclidiana. O treinamento dos modelos estão no arquivo randomforest_knn.py . Depois do treinamento, o programa automaticamente salva os modelos, com auxílio da biblioteca joblib pois eles serão usados para classifição no arquivo chatbot.py.<br>
&emsp;&emsp;Para o desenvolvimento do chatbot, fiz uma rede neural simples, com três camadas densas e duas de dropout, utilizei o Adam como otimizador com um learning rate de 0.01 ,pois foi o melhor otimizador que tinha encontrado quando fiz o trabalho 4 dessa disciplina(testei com o SGD também, porém o desempenho do Adam foi melhor). O treinamento do chatBot é feito no arquivo trainingBot.py e a aplicação do chatBot é feito no arquivo chatBot.py. Tive que fazer o chatbot em inglês, pois utilizei o método WordLemmatizer, da biblioteca nltk, cuja função é agrupar as formas flexionadas de uma palavra para que possam ser analisadas como um único item, por exemplo, no inglês temos várias variações da palavra 'work', como 'works, 'worked', 'working', esse método pega todas essas palavras para serem analisada como 'work', não achei uma maneira fácil de usar esse método na língua portuguesa, logo peço perdão caso encontre algum erro no inglês. <br>
&emsp;&emsp;Para finalizar, o programa chatbot.py, após pegar todos os dados, como informações pessoais e sintomas do paciente, gera um arquivo docx, que seria a ficha médica do paciente. <br>

## Resultados
&emsp;&emsp; Em relação ao KNN e ao random forest, escolhi várias métricas para podermos analisarmos a eficácia, para não ter problema de confiarmos em apenas uma e termos uma falsa impressão que o modelo está satisfatório. Lembrando que: {0 : Alergia, 1 : Resfriado, 2 : COVID, 3 : GRIPE}<br>
&emsp;&emsp;<b>Random Forest</b>:Tem uma média de eficácia do modelo de 93% e podemos observar na matriz de confusão que os verdadeiros positivos e negativos ocorrem com bastante mais frequência que os falsos positivos e negativos, os casos de gripe que tem mais tendência a erro facilmente confundidos por COVID <br>

<code>
---------------- Random Forest ----------------
              precision    recall  f1-score   support

           0       0.96      0.98      0.97       211
           1       0.93      0.94      0.93       211
           2       0.88      0.93      0.91       211
           3       0.96      0.88      0.92       211

    accuracy                           0.93       844
   macro avg       0.93      0.93      0.93       844
weighted avg       0.93      0.93      0.93       844
</code>
<br>

<figure align="right" >
    <img src="imagens/ConfusionMatrixRF.png" alt="sem under sampling"  height= "250">
    <figcaption>Matriz de confusão do Random Forest</figcaption>
</figure><br>
 
&emsp;&emsp;<b>K-Nearest neighbor</b>:Tem uma média de eficácia do modelo de 86% e podemos observar na matriz de confusão que os verdadeiros positivos e negativos ocorrem com bastante mais frequência que os falsos positivos e negativos, os casos de gripe que tem mais tendência a erro facilmente confundidos por COVID e resfriados.<br>
<code>
---------------- K-Nearest neighbor ----------------
              precision    recall  f1-score   support

           0       1.00      0.87      0.93       211
           1       0.78      1.00      0.88       211
           2       0.77      0.96      0.85       211
           3       1.00      0.60      0.75       211

    accuracy                           0.86       844
   macro avg       0.89      0.86      0.85       844
weighted avg       0.89      0.86      0.85       844
</code>
<br>
<figure align="right" >
    <img src="imagens/ConfusionMatrixKNN.png" alt="sem under sampling"  height= "250">
    <figcaption>Matriz de confusão do Random Forest</figcaption>
 </figure><br>
 
 &emsp;&emsp;Para rede neural utilizada para a construção do chatBot, temos uma acurácia de 98.25% após o treinamento de 200 epócas.<br>
<code>
Epoch 1/100 <br>
12/12 [==============================] - 1s 2ms/step - loss: 2.0453 - accuracy: 0.2281 <br>
Epoch 2/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 1.7778 - accuracy: 0.4035 <br>
Epoch 3/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 1.4486 - accuracy: 0.5088 <br>
Epoch 4/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 1.0473 - accuracy: 0.6842 <br>
Epoch 5/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.7694 - accuracy: 0.7544 <br>
Epoch 6/100 <br>
12/12 [==============================] - 0s 3ms/step - loss: 0.6967 - accuracy: 0.7368 <br>
Epoch 7/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.4201 - accuracy: 0.8596 <br>
Epoch 8/100 <br>
12/12 [==============================] - 0s 4ms/step - loss: 0.2586 - accuracy: 0.9474 <br>
Epoch 9/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2749 - accuracy: 0.9298 <br>
Epoch 10/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.3427 - accuracy: 0.8772 <br>
Epoch 11/100 <br>
12/12 [==============================] - 0s 1ms/step - loss: 0.2164 - accuracy: 0.9123 <br>
Epoch 12/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1798 - accuracy: 0.9298 <br>
Epoch 13/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2381 - accuracy: 0.9123 <br>
Epoch 14/100 <br>
12/12 [==============================] - 0s 1ms/step - loss: 0.2199 - accuracy: 0.8596 <br>
Epoch 15/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2347 - accuracy: 0.9474 <br>
Epoch 16/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1487 - accuracy: 0.9825 <br>
Epoch 17/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1959 - accuracy: 0.9474 <br>
Epoch 18/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1510 - accuracy: 0.9474 <br>
Epoch 19/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1690 - accuracy: 0.9474 <br>
Epoch 20/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1701 - accuracy: 0.9298 <br>
Epoch 21/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0837 - accuracy: 0.9649 <br>
Epoch 22/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0232 - accuracy: 1.0000 <br>
Epoch 23/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0664 - accuracy: 0.9649 <br>
Epoch 24/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0539 - accuracy: 0.9649 <br>
Epoch 25/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0805 - accuracy: 0.9649 <br>
Epoch 26/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1295 - accuracy: 0.9649 <br>
Epoch 27/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1153 - accuracy: 0.9649 <br>
Epoch 28/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2349 - accuracy: 0.9474 <br>
Epoch 29/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1176 - accuracy: 0.9825 <br>
Epoch 30/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0626 - accuracy: 0.9825 <br>
Epoch 31/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2018 - accuracy: 0.9474 <br>
Epoch 32/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2196 - accuracy: 0.9649 <br>
Epoch 33/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2463 - accuracy: 0.9649 <br>
Epoch 34/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1690 - accuracy: 0.9474 <br>
Epoch 35/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2359 - accuracy: 0.9474 <br>
Epoch 36/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1023 - accuracy: 0.9825 <br>
Epoch 37/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0949 - accuracy: 0.9825 <br>
Epoch 38/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1134 - accuracy: 0.9649 <br>
Epoch 39/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1805 - accuracy: 0.9298 <br>
Epoch 40/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0570 - accuracy: 0.9825 <br>
Epoch 41/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0529 - accuracy: 0.9825 <br>
Epoch 42/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0832 - accuracy: 0.9649 <br>
Epoch 43/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0331 - accuracy: 1.0000 <br>
Epoch 44/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0498 - accuracy: 0.9649 <br>
Epoch 45/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0491 - accuracy: 0.9825 <br>
Epoch 46/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0723 - accuracy: 0.9474 <br>
Epoch 47/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0846 - accuracy: 0.9474 <br>
Epoch 48/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0933 - accuracy: 0.9474 <br>
Epoch 49/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0469 - accuracy: 0.9825 <br>
Epoch 50/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0543 - accuracy: 0.9825 <br>
Epoch 51/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0387 - accuracy: 0.9825 <br>
Epoch 52/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1329 - accuracy: 0.9474 <br>
Epoch 53/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0476 - accuracy: 1.0000 <br>
Epoch 54/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0939 - accuracy: 0.9474 <br>
Epoch 55/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0512 - accuracy: 0.9825 <br>
Epoch 56/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1091 - accuracy: 0.9474 <br>
Epoch 57/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0597 - accuracy: 0.9825 <br>
Epoch 58/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0659 - accuracy: 0.9649 <br>
Epoch 59/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0336 - accuracy: 0.9825 <br>
Epoch 60/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0988 - accuracy: 0.9474 <br>
Epoch 61/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0961 - accuracy: 0.9649 <br>
Epoch 62/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0660 - accuracy: 0.9474 <br>
Epoch 63/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2421 - accuracy: 0.9123 <br>
Epoch 64/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0685 - accuracy: 0.9649 <br>
Epoch 65/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1687 - accuracy: 0.9474 <br>
Epoch 66/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0682 - accuracy: 0.9474 <br>
Epoch 67/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0365 - accuracy: 0.9825 <br>
Epoch 68/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0474 - accuracy: 1.0000 <br>
Epoch 69/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0780 - accuracy: 0.9649 <br>
Epoch 70/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0607 - accuracy: 0.9649 <br>
Epoch 71/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0730 - accuracy: 0.9649 <br>
Epoch 72/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0543 - accuracy: 0.9649 <br>
Epoch 73/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0328 - accuracy: 0.9825 <br>
Epoch 74/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1422 - accuracy: 0.9649 <br>
Epoch 75/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0918 - accuracy: 0.9649 <br>
Epoch 76/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1991 - accuracy: 0.9474 <br>
Epoch 77/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0222 - accuracy: 0.9825 <br>
Epoch 78/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1473 - accuracy: 0.9298 <br>
Epoch 79/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1072 - accuracy: 0.9649 <br>
Epoch 80/100 <br>
12/12 [==============================] - 0s 1ms/step - loss: 0.0910 - accuracy: 0.9825 <br>
Epoch 81/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0554 - accuracy: 0.9649 <br>
Epoch 82/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1140 - accuracy: 0.9649 <br>
Epoch 83/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0929 - accuracy: 0.9825 <br>
Epoch 84/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0358 - accuracy: 0.9825 <br>
Epoch 85/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2528 - accuracy: 0.9123 <br>
Epoch 86/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0476 - accuracy: 0.9825 <br>
Epoch 87/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0566 - accuracy: 0.9649 <br>
Epoch 88/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0430 - accuracy: 0.9649 <br>
Epoch 89/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0245 - accuracy: 1.0000 <br>
Epoch 90/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0595 - accuracy: 0.9649 <br>
Epoch 91/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0246 - accuracy: 0.9825 <br>
Epoch 92/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0368 - accuracy: 0.9825 <br>
Epoch 93/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0187 - accuracy: 1.0000 <br>
Epoch 94/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1179 - accuracy: 0.9474 <br>
Epoch 95/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.2349 - accuracy: 0.9298 <br>
Epoch 96/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0602 - accuracy: 0.9649 <br>
Epoch 97/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0887 - accuracy: 0.9649 <br>
Epoch 98/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1035 - accuracy: 0.9649 <br>
Epoch 99/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.0724 - accuracy: 0.9474 <br>
Epoch 100 <br>/100 <br>
12/12 [==============================] - 0s 2ms/step - loss: 0.1765 - accuracy: 0.9825 <br>
Training complete <br>
</code>

## Conclusão
&emsp;&emsp; Apesar dos modelos terem eficácias altas, existem muitos casos de gripe e resfriados que são confundidos com COVID e como o COVID é uma doença altamente contagiosa, que foi responsável por uma pandemia que parou o mundo inteiro, talvez não seja muito aconselhável confiar no diagnóstico de COVID, gripe e resfriado, já que são confundidos com uma frequência maior que eu esperava. Porém, os modelos foram excelentes em separar esses casos da alergia, o que é bom porque a alergia tem sintomas bem semelhantes ao COVID. 


## Referências
https://sigmoidal.ai/como-lidar-com-dados-desbalanceados/ <br>
https://www.youtube.com/watch?v=1lwddP0KUEg&t=1737s

## Responsáveis
- [Luísa de Souza Ferreira](https://github.com/ferreiraluisa)

