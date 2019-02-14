from gensim.models.keyedvectors import KeyedVectors
import logging
from scipy import stats
import numpy as np
from sklearn import metrics

file = input('The vector file:')
model = KeyedVectors.load_word2vec_format(file, binary=False)

#verbs
similar = model.most_similar('击败')
print('击败：')
print(similar)
print('\n')
similar = model.most_similar('引用')
print('引用：')
print(similar)
print('\n')
similar = model.most_similar('研究')
print('研究：')
print(similar)
print('\n')
similar = model.most_similar('形成')
print('形成：')
print(similar)
print('\n')
similar = model.most_similar('增加')
print('增加：')
print(similar)
print('\n')

#nouns
similar = model.most_similar('文化')
print('文化：')
print(similar)
print('\n')

similar = model.most_similar('经济')
print('经济：')
print(similar)
print('\n')

similar = model.most_similar('人口')
print('人口：')
print(similar)
print('\n')

similar = model.most_similar('工作')
print('工作：')
print(similar)
print('\n')

similar = model.most_similar('海')
print('海：')
print(similar)
print('\n')

#adjective
similar = model.most_similar('深')
print('深：')
print(similar)
print('\n')

similar = model.most_similar('重要')
print('重要：')
print(similar)
print('\n')

similar = model.most_similar('高')
print('高：')
print(similar)
print('\n')

similar = model.most_similar('新')
print('新：')
print(similar)
print('\n')

similar = model.most_similar('相似')
print('相似：')
print(similar)
print('\n')


#other pos tag
similar = model.most_similar('两')
print('两：')
print(similar)
print('\n')

similar = model.most_similar('东')
print('东：')
print(similar)
print('\n')

similar = model.most_similar('次')
print('次：')
print(similar)
print('\n')

similar = model.most_similar('一片')
print('一片：')
print(similar)
print('\n')

similar = model.most_similar('那个')
print('那个：')
print(similar)
print('\n')
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#msgs = model.accuracy('semantic')


