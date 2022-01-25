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

#extract topic formulas (test data)
data_test = pd.read_csv(r'''/Users/Vidya_Thesis/data/topics_output.tsv''', sep='\t')

formulas_test = []
for index, row in data_test.iterrows():
    formulas_test.append(str(row['Latex']))  # x+y=z


cleaned_data_test = [x for x in formulas_test if isinstance(x, str)]  # remove nan from the list
cleaned_data_test = set(cleaned_data_test)
all_formulas_test = []
for each_formula in cleaned_data_test:
    f =[]
    f.append(each_formula)
    all_formulas_test.append(f)

print(len(all_formulas_test))

#training data 
tokens_model = Word2Vec (allTokens, window=10, min_count=2, workers=10)
tokens_model.train(allTokens,total_examples=len(allTokens),epochs=10)

w1 = "q"
print(tokens_model.wv.most_similar (positive=w1))

w1 = ['V', '^', '{', 'H', '}', '*', 'V', '=']
w2 = ['a']
print(tokens_model.wv.most_similar (positive=w1,negative=w2,topn=10))

f = open("TokenOutput.txt", "w")
f.write("Query formula"+"\t"+"Similar formulas")

for each_test_formula in all_formulas_test:
  query = each_test_formula
  similar_formulas = tokens_model.wv.most_similar (positive=query,topn=1000)
  f.write(w1+"\t"+similar_formulas)
f.close()

