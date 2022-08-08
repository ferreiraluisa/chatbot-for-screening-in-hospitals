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
Projeto final apresentado à disciplina de Inteligência Artificial I, de código INF 420, ministrada pelo professor Julio C. S. Reis, como requisito parcial para aprovação na disciplina.

## Introdução
O trabalho proposto é um chatbot responsável por fazer triagem em hospitais para diferenciar os casos de COVID entre os seguintes casos com sintomas semelhantes: alergia, resfriado e gripe. Além disso, no final, ele gera uma ficha médica do paciente com informações pessoais, como nome, idade, profissão, os sintomas, quantos dias ele está doente e resultado da predição feito com técnicas de inteligência artificial. 
 
## Metodologia
Utilizei um <a href="https://www.kaggle.com/datasets/walterconway/covid-flu-cold-symptoms">dataset</a> disponível no Kaggle, com vários casos de enfermidade junto aos seus sintomas e a classificação de cada um dos casos como alergia, resfriado, covid ou gripe. Essa base de dados está desbalanceada, existem muitos casos de alergia em comparação com covid, resfriado e gripe,isso é um problema pois pode gerar muitos "alarmes falsos", o diagnóstico acabaria tendenciando muito para alergia, pois tem muitas amostras e por os sintomas entre as quatro enfermidades serem bem semelhantes, além de dificultar a avaliação de eficácia. Por isso, utilizei a técnica de under-sampling, com o método RandomUnderSampler() da biblioteca imblearn.under_sampling.
    <img src="imagens/sem_under_sampling.png" alt="sem under sampling" align="right" height="55" />
    <img src="imagens/com_under_sampling.png" alt="sem under sampling" align="left" height="55" />
    

## Resultados

## Conclusão





## Referências
https://www.kaggle.com/code/vishakhasinghiitbhu/covid-classifier
https://sigmoidal.ai/como-lidar-com-dados-desbalanceados/
https://www.kaggle.com/datasets/walterconway/covid-flu-cold-symptoms

## Responsáveis
- [Luísa de Souza Ferreira](https://github.com/ferreiraluisa)

