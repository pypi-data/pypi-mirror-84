from collections import Counter
from itertools import chain
import math
import numpy as np
import nltk
nltk.download('punkt')
from nltk import word_tokenize 
from nltk.util import ngrams

import pandas as pd
import numpy as np

class Vectorizer:
  def __init__(self):
    """
       USAGE:
      --------
      from SecVectorizer import Vectorizer
      vec = Vectorizer()
      x_train = vec.fit_transform(train_sentences)
      x_test = vec.transform(test_sentences)
      ----------------------------------------
      vec.get_features() #to get the vocabulary
    """
  def fit_transform(self, data, num_of_sequence=1, accelerator=1.7):
    self.countDict = {}
    
    l_data = list(data)
    for line in l_data:
      for  word in nltk.word_tokenize(line):
        if word in self.countDict:
          self.countDict[word]+=1
        else:
          self.countDict[word]=1

    self.nested_dict={}

    for i in range(len(data)):
      line = "# " + data[i]
      token = nltk.word_tokenize(line)
      temp_dict = Counter(token)
      bigram =  list(ngrams(token, 2)) 
      total_sn = len(data)

      for b in bigram:
        #print(line)
        if b[0] == '#':
          devide = total_sn
        else: 
          devide = self.countDict[b[1]]
        try:
          if b[0] in self.nested_dict[b[1]]:
            self.nested_dict[b[1]].update({b[0] : self.nested_dict[b[1]][b[0]]+(1 / devide) } )
          else:
            self.nested_dict[b[1]].update( {b[0] : (1 / devide)} )
        except:
            self.nested_dict[b[1]] = {b[0] : (1 / devide)}
        
        
    df = pd.DataFrame(np.array( [np.zeros(len(data))]* (len(self.nested_dict.keys())) ).T, columns = list(self.nested_dict.keys()))
    if num_of_sequence==1:
      for i,line in enumerate(data):
        line = "#" + line
        token = nltk.word_tokenize(line)
        temp_dict = Counter(token)
        for j in range(1,len(token)):
          if j ==1:
            df[token[j]][i] +=   math.exp(self.nested_dict[token[j]][token[j-1]]) #/temp_dict[token[j]]
          else:
            x = float(df[token[j-1]][i])
            df[token[j]][i] +=  math.exp(self.nested_dict[token[j]][token[j-1]] * (accelerator/(1+np.exp(-x)))) 
    else:
      for i,line in enumerate(data):
        line = "#" + line
        token = nltk.word_tokenize(line)
        temp_dict = Counter(token)
        
        for j in range(1,len(token)):
          if j ==1:
            df[token[j]][i] +=   math.exp(self.nested_dict[token[j]][token[j-1]]) #/temp_dict[token[j]]
          elif j==2:
            x = float(df[token[j-1]][i])
            df[token[j]][i] +=  math.exp(self.nested_dict[token[j]][token[j-1]] * (accelerator/(1+np.exp(-x)))) 
          else:
            x = float(df[token[j-1]][i])
            y = float(df[token[j-2]][i])
            df[token[j]][i] +=  math.exp(self.nested_dict[token[j]][token[j-1]] * (accelerator/(1+np.exp(-x)))) 
            a = math.exp(self.nested_dict[token[j]][token[j-1]] * (accelerator/(1+np.exp(-x)))) 
            try:
              b = math.exp(self.nested_dict[token[j]][token[j-2]] * (accelerator/(1+np.exp(-y))))
            except:
              b = (accelerator/(1+np.exp(-y)))

            df[token[j]][i] += max(a,b)
    
    return df.values



  def transform(self,data): 
    len(data)   
    df = pd.DataFrame(np.array( [np.zeros(len(data))]* (len(self.nested_dict.keys())) ).T, columns = list(self.nested_dict.keys()))

    for i,line in enumerate(data):
      line = "#" + line
      token = nltk.word_tokenize(line)
      temp_dict = Counter(token)
      
      for j in range(1,len(token)):
        #print(token[j], token[j-1])
        try:
          if j==1:
            df[token[j]][i] += (self.nested_dict[token[j]][token[j-1]]) #/temp_dict[token[j]]
          else:
            x = float(df[token[j-1]][i])
            df[token[j]][i] +=  math.exp(self.nested_dict[token[j]][token[j-1]]  * (1.7/(1+np.exp(-x))))
        except:
          if token[j] in df.columns:
            devide = self.countDict[token[j]]
            self.nested_dict[token[j]].update({token[j-1] : (1 / devide)})
            df[token[j]][i] += 1/devide
    return df.values

  def get_features(self):
    return self.nested_dict.keys()
    