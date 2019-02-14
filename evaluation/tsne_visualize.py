from gensim.models.keyedvectors import KeyedVectors
from sklearn.manifold import TSNE 
from sklearn.datasets import fetch_20newsgroups 
import re 
import matplotlib.pyplot as plt 


file = input('The vector file:')
model = KeyedVectors.load_word2vec_format(file, binary=False)

X = model[model.wv.vocab]

tsne = TSNE(n_components=2) 
X_tsne = tsne.fit_transform(X) 

plt.scatter(X_tsne[:, 0], X_tsne[:, 1]) 
plt.show() 

