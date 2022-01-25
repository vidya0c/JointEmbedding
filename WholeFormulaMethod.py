# whole formula is used for training

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
all_formulas = []
for each_formula in cleaned_data:
    f =[]
    f.append(each_formula)
    all_formulas.append(f)
    
print(len(all_formulas))

full_formula_model = Word2Vec (all_formulas, min_count=1)
full_formula_model.train(all_formulas,total_examples=len(all_formulas),epochs=10)

print(len(full_formula_model.wv.vocab)) #vocabulary size

w1 = "f(x)"
print(full_formula_model.wv.most_similar (positive=w1,topn=10))

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

f = open("WholeFormulaOutput.txt", "w")
f.write("Query formula"+"\t"+"Similar formulas")

for each_test_formula in all_formulas_test:
  query = each_test_formula
  similar_formulas = full_formula_model.wv.most_similar (positive=query,topn=1000)
  f.write(w1+"\t"+similar_formulas)
f.close()

