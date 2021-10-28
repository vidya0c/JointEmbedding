from gensim.models import Word2Vec
import pandas as pd
from transvec.transformers import TranslationWordVectorizer
from gensim.models import KeyedVectors

data = pd.read_csv("/Users/vishwanathlhugar/Vidya_Thesis/data/new_output_file.tsv", sep='\t')
formulas = []
all_formulas = []
context_words = []


for index, row in data.iterrows():
    all_formulas.append(row['question'])
    all_formulas.append(row['answer'])
    op = (str(row['answer_CW'])).strip('][').split(', ')
    context_words.append(op)

#print(context_words[:100])

# formulas to train
data = [x for x in all_formulas if isinstance(x, str)] # remove nan from the list
formulas.append(data)

# train model for formulas and words separately
formula_model = Word2Vec(formulas, min_count=1)
word_model = Word2Vec(context_words, min_count=1)

# summarize the loaded model
print("Formula Model:", formula_model)
#print("Formula Model Length:", len(formula_model.wv.vocab.keys()))
print("Word Model:", word_model)
#print("Word Model Length:", len(word_model.wv.vocab.keys()))

# summarize vocabulary
#print("Formulas:", list(formula_model.wv.vocab.keys()))
#print("Context words:", list(word_model.wv.vocab.keys()))

all_normed_vectors = formula_model.wv.vectors
#print("Vectors:", all_normed_vectors)
# # access vector for one word

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

#
# The more you can provide, the better.
train = [
    ("\sqrt{2}", "'contradiction.'", "'Basically,'", "'you'", "'suppose'", "'that'", "'can'", "'be'", "'written'", "'as'", "'p/q.'"),
    ("\int_{x=0}^{\sqrt{2}} (2\pi y) ds = \int_{0}^{\sqrt{2}} 2 \pi x^2 \sqrt{1+(2x)^2} dx", "'bit'", "'help:'", "'surface'", "'area'", "'and'", "'antiderivate'"),
    ("\ln | \sqrt{1+4x^2}+2x |","'2x'", "'snuck'", "'radical'", "'accident,'", "'term'","'fix'")]

bilingual_model = TranslationWordVectorizer(reloaded_formula_model_vectors, reloaded_word_model_vectors).fit(train)

# Find words with similar meanings across both languages.
print("bilingual_model:",bilingual_model.similar_by_word("\\sqrt{2}", 1))

# load model
# new_model = Word2Vec.load('formula_model.bin')
# print("loaded Model", new_model)
# more_sentences = [
#     ['vec p_1', 'theta', 'vec p_2', 'sqrt{2}',
#      'v = arccosleft(frac{x_1x_2 + y_1y_2}{sqrt{(x_1^2+y_1^2) cdot (x_2^2+y_2^2)}}right)',
#      'v = arccosleft(frac{x_1x_2 + y_1y_2 + z_1z_2}{sqrt{(x_1^2+y_1^2+z_1^2) cdot (x_2^2+y_2^2+z_2^2)}}right)',
#      'theta = arccosleft(frac{vec p_1 cdot vec p_2}{|vec p_1| cdot |vec p_2|}right)',
#      'vec p_1cdot vec p_2 = |vec p_1| cdot |vec p_2| cdot cos theta'],
# ]
# new_model.build_vocab(more_sentences, update=True)
# new_model.train(more_sentences, total_examples=new_model.corpus_count, epochs=new_model.epochs)
#
# model_with_loss = Word2Vec(
#     formulas,
#     min_count=1,
#     compute_loss=True,
#     hs=0,
#     sg=1,
#     seed=42,
# )
#
# # getting the training loss value
# training_loss = model_with_loss.get_latest_training_loss()
# print(training_loss)
