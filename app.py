#54. Веб-сервис, который выбирает случайные слова и просит пользователя найти лишнее.
#Сервис сравнивает с выбором word2vec и запоминает результат сравнения
#можно посмотреть статистику на отдельной странице).

from flask import Flask
from flask import url_for, render_template, request, redirect
import random
import sys
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import networkx as nx 

app = Flask(__name__)

@app.route('/')
def index():
    urls = {'главная (эта страница)': url_for('index'),
            'форма (форма и ответ на одном url)': url_for('form'),}
    return render_template('index.html', urls=urls)

@app.route("/form")
def form():
    m = 'ruscorpora_upos_skipgram_300_10_2017.bin.gz'
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    words = []
    for i in range(5):
        words = words.append(random.choice(model))
    word0 = words[0]
    word1 = words[1]
    word2 = words[2]
    word3 = words[3]
    word4 = words[4]
    if request.args:
        user_name = request.args['name']
        user_choice = request.args['answer']
        num = int(user_choice)
        extraneous = words[num]
        string = ''
        for el in words:
            string = string + el
            string = string + ' '
        vec_choice = model.doesnt_match(string.split())
        with open("choices.txt", "a", encoding='utf-8') as g:
            g.write('Пользователь ' + user_name + ' из представленных слов: ')
            g.write(word0 + ', ' + word1 + ', ' + word2 + ', ' + word3 + ', ' + word4)
            g.write(' выбрал лишним слово ' + extraneous + ', а модель считает лишним слово ' + vec_choice + '. ')
        with open("choices.txt", "r", encoding='utf-8') as f:
            content = f.read()
        return render_template("choices.html", content=content)
    return render_template('form.html', word0=word0, word1=word1, word2=word2, word3=word3, word4=word4)

if __name__ == '__main__':
    app.run(debug=True)




