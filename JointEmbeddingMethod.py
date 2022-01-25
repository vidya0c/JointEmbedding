from gensim.models import Word2Vec
import pandas as pd
from transvec.transformers import TranslationWordVectorizer
from gensim.models import KeyedVectors

data = pd.read_csv("/Users/Vidya_Thesis/data/preprocessed.tsv", sep='\t')
formulas = []
all_formulas = []
context_words = []


for index, row in data.iterrows():
    all_formulas.append(row['question'])
    all_formulas.append(row['answer'])
    op = (str(row['answer_CW'])).strip('][').split(', ')
    context_words.append(op)


# formulas to train
data = [x for x in all_formulas if isinstance(x, str)] # remove nan from the list
formulas.append(data)

# train model for formulas and words separately
formula_model = Word2Vec(formulas, min_count=1)
formula_model.train(all_formulas,total_examples=len(all_formulas),epochs=10)

word_model = Word2Vec(context_words, min_count=1)
word_model.train(context_words,total_examples=len(context_words),epochs=10)

# summarize the loaded model
print("Formula Model:", formula_model)
print("Formula Model Length:", len(formula_model.wv.vocab.keys()))

print("Word Model:", word_model)
print("Word Model Length:", len(word_model.wv.vocab.keys()))

# summarize vocabulary
print("Formulas:", len(formula_model.wv.vocab))
print("Context words:", len(word_model.wv.vocab))

all_normed_vectors = formula_model.wv.vectors
# access vector for one word

print("Similarities :", formula_model.wv.most_similar('O(\log \log n)', topn=5))
#save model
formula_model.save('formula_model.bin')
word_model.save('word_model.bin')

formula_model_vectors = formula_model.wv
word_model_vectors = word_model.wv


formula_model_vectors.save('formula_model_vectors.kv')
reloaded_formula_model_vectors = KeyedVectors.load('formula_model_vectors.kv')

word_model_vectors.save('word_model_vectors.kv')
reloaded_word_model_vectors = KeyedVectors.load('word_model_vectors.kv')

#more formulas to train
train = [
    ("\sqrt{2}", "'contradiction.'", "'Basically,'", "'you'", "'suppose'", "'that'", "'can'", "'be'", "'written'", "'as'", "'p/q.'"),
    ("\int_{x=0}^{\sqrt{2}} (2\pi y) ds = \int_{0}^{\sqrt{2}} 2 \pi x^2 \sqrt{1+(2x)^2} dx", "'bit'", "'help:'", "'surface'", "'area'", "'and'", "'antiderivate'"),
    ("\ln | \sqrt{1+4x^2}+2x |","'2x'", "'snuck'", "'radical'", "'accident,'", "'term'","'fix'")]

#Joint embedding using Translational Model
joint_embedding_model = TranslationWordVectorizer(reloaded_formula_model_vectors, reloaded_word_model_vectors).fit(train)

# Find words with similar meanings across both languages.
print("bilingual_model:",joint_embedding_model.similar_by_word("\\sqrt{2}", 1))

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

f = open("JointEmbeddingOutput.txt", "w")
f.write("Query formula"+"\t"+"Similar formulas")

for each_test_formula in all_formulas_test:
  query = each_test_formula
  similar_formulas = joint_embedding_model.wv.most_similar (positive=query,topn=1000)
  f.write(w1+"\t"+similar_formulas)
f.close()
