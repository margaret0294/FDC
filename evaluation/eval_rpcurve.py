from gensim.models.keyedvectors import KeyedVectors
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

file1 = input('The vector file:')
file2 = input('The fdc vector file:')
print('wordsim dataset is 297.txt')
model1 = KeyedVectors.load_word2vec_format(file1, binary=False)
model2 = KeyedVectors.load_word2vec_format(file2, binary=False)

wordsimfile = '#297.txt'

sentence = [[]]
y_score = []

#get the words similar dataset
for line in open(wordsimfile, 'r').readlines():
    if line != '\n':
        word = line.split()
        sentence.append(word)
    if sentence[0] == []:
        sentence.pop(0)
    if float(word[2])*2/10 >= 0.4: #297.txt
        y_score.append(1)
    else:
        y_score.append(0)

def prc (sentence, model, y_score):
    y_test = []
    for i in range(len(sentence)):
        if sentence[i][0] in model.wv.vocab:
            if sentence[i][1] in model.wv.vocab:
                y_test.append(model.similarity(sentence[i][0], sentence[i][1]))
            else:
                y_test.append(0)
        else:
            y_test.append(0)
    precision, recall, _ = precision_recall_curve(y_score, y_test)
    return precision, recall
#y_score = ay / 10  #240.txt

precision1, recall1 = prc(sentence, model1, y_score)
precision2, recall2 = prc(sentence, model2, y_score)


lines = []
labels = []

plt.figure()


l, = plt.plot(recall1, precision1, color='cornflowerblue', lw = 2)
lines.append(l)
labels.append('original vector')

l, = plt.plot(recall2, precision2, color='darkorange', lw = 2)
lines.append(l)
labels.append('Fixed-point vector')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.0])
plt.xlim([0.0, 1.0])
plt.title('Precision-Recall curve')
plt.legend(lines, labels, loc='upper right')

plt.show()