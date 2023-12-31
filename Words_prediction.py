#------------------------------------
# Прогнозирование слов (RNN), Embedding
#------------------------------------
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from keras.layers import Dense,SimpleRNN,Embedding
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical


with open('text_files/just_text.txt', 'r', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')  # убираем первый невидимый символ

maxWordsCount = 1000
tokenizer = Tokenizer(num_words=maxWordsCount, lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts([texts]) # делаем токенезацию (разбиваем текст на слова)

# просмотреть сколько раз какое слово встречается в тексте
# dct = list(tokenizer.word_counts.items())
# print(dct[:10])

data = tokenizer.texts_to_sequences([texts]) # текст -> в последовательность чисел
res = np.array( data[0] )

inp_words = 3
n = res.shape[0] - inp_words

X = np.array([res[i:i + inp_words] for i in range(n)])
Y = to_categorical(res[inp_words:], num_classes=maxWordsCount) # one-hot вектора

model = Sequential()
model.add(Embedding(maxWordsCount, 256, input_length = inp_words))
model.add(SimpleRNN(128, activation='tanh'))
model.add(Dense(maxWordsCount, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
history = model.fit(X, Y, batch_size=32, epochs=50)


def buildPhrase(texts, str_len=20):
    res = texts
    data = tokenizer.texts_to_sequences([texts])[0]
    for i in range(str_len):
        x = data[i: i + inp_words]
        inp = np.expand_dims(x, axis=0)

        pred = model.predict(inp)
        indx = pred.argmax(axis=1)[0]
        data.append(indx)
        res += " " + tokenizer.index_word[indx]  # дописываем строку

    return res


res = buildPhrase("надо иметь цель")
print(res)