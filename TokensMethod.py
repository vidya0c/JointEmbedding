# formula divided as tokens to train 

from io import StringIO
import tokenize
import pandas as pd
from gensim.models import Word2Vec


#read data from preprocessed file 
data = pd.read_csv(r'''/Users/Vidya_Thesis/data/preprocessed.tsv''', sep='\t')

formulas = []
for index, row in data.iterrows():
    formulas.append(str(row['question']))  # x+y=z
    formulas.append(str(row['answer']))

cleaned_data = [x for x in formulas if isinstance(x, str)]  # remove nan from the list
cleaned_data = set(cleaned_data)

    
allTokens = []

for formula in cleaned_data:
    listofTokens = []
    tokens = tokenize.generate_tokens(StringIO(formula).readline)  # divide tokens as x,+,y,=,z

    try:
        for t in tokens:
            if len(t[1]) > 0:
                listofTokens.append(t[1])
        allTokens.append(listofTokens)
    except:
        continue

print(len(allTokens))  #vocabulary size

formula_model = Word2Vec (allTokens, window=10, min_count=2, workers=10)
formula_model.train(allTokens,total_examples=len(allTokens),epochs=10)

w1 = "q"
print(formula_model.wv.most_similar (positive=w1))

w1 = ['V', '^', '{', 'H', '}', '*', 'V', '=']
w2 = ['a']
print(formula_model.wv.most_similar (positive=w1,negative=w2,topn=10))
