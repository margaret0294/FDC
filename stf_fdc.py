# -*- coding:utf8 -*-
#get rid of functional words

#define pos(stanford parser) tag of functional words
func_words = ['AD',  #adverbs
              'AS',  #aspect marker
              'BA',  #ba-const
              'CC',  #coordination conjunction
              'CS',  #subordinating conj
              'DEC', #for relative-clause etc
	      'DEG', #associative
	      'DER', #in V-de constructive and V-de-R
	      'DEV', #Before VP
              'IJ',  #Interjection
              'LB',  #in long bei-construction
              'MSP', #particles
              'ON',  #Onomatopoeia
              'P',   #prepositions
              'SB',  #in long bei-consturction
              'SP'   #sentence-final particle
              ]


def fdc(sentence):
    func_index = []
    for i in range(len(sentence)):
        if sentence[i][4] in func_words: #pos tag position
            func_index.append(i) #record functional word's position in the sentence
            parent = sentence[i][6] #parent node
            for j in range(len(sentence)):
                if sentence[j][6] == sentence[i][0]:# whether the node have child nodes
                    sentence[j][6] = parent
    #delete functional word
    func_index.reverse()
    for i in range (len(func_index)):
        sentence.pop(func_index[i])

    #renumber
    index = 1
    for i in range(len(sentence)):
        sentence[i][0] = index
        if int(sentence[i][6]) > len(sentence):
            sentence[i][6] = len(sentence)
        index = index + 1

def print_conll(sentence,f):
    for i in range(len(sentence)):
        for j in range(10):
            print(sentence[i][j], file = f, end='\t')
        f.write('\n')
    f.write('\n')

sentence = [[]]
i = 0
for line in open('./filter_abc.out', 'r').readlines():

    if line != '\n': #separate each sentence 
       word = line.split()
       sentence.append(word)
    else:
        if sentence[0] == []:
           sentence.pop(0)
        fdc(sentence)
        i = i+1

        with open('./fdc_filter.out', 'a') as f:
            print_conll(sentence,f)
        if i % 1000 == 0:
            print('Finished ' + str(i) + ' lines')

        sentence.clear()
        f.close()



