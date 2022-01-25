from gensim.parsing.preprocessing import remove_stopwords
from QAClass import QAClass
from xmlr.xmlr import xmliter

from QuestionAnswerParser import QuestionAnswerParser


def getFormulaAndContextWords(post_ID, type_ID, html, window_size, qa_object_list):
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.findAll("span"):
        all_questions = []
        all_answers = []
        n_side = int(window_size / 2)

        text = soup.text.replace('\n', ' ')
        filtered_sentence = remove_stopwords(text)  # remove stop words

        if len(i.text)!=0:
            context_before = filtered_sentence.split(i.text)[0]
            words_before = list(filter(bool, context_before.split(" ")))

            context_after = text.split(i.text)[1]
            words_after = list(filter(bool, context_after.split(" ")))

            if len(words_after) >= n_side:
                words_before = words_before[-n_side:]
                words_after = words_after[:(window_size - len(words_before))]
            else:
                words_after = words_after[:n_side]
                words_before = words_before[-(window_size - len(words_after)):]

            if type_ID == 1:
                question = QAClass()
                question.updateFormulaAndContextWords(i.text, words_before + words_after)
                all_questions.append(question)
            else:
                answer = QAClass()
                answer.updateFormulaAndContextWords(i.text, words_before + words_after)
                all_answers.append(answer)

            qa_object_list = findObject(qa_object_list, post_id, post_type_id, all_questions, all_answers)

    return


# Create or return the qa_object
def findObject(qa_obj_list, post_id, post_type_id, QList, AList):
    for obj in qa_obj_list:
        if obj.ID == post_id:
            obj.updateList(post_type_id, QList, AList)
            return qa_obj_list

    qa_obj = QuestionAnswerParser(post_id, post_type_id, QList, AList)
    qa_obj_list.append(qa_obj)
    return qa_obj_list


if __name__ == '__main__':

    delimiter = "\t"
    xml_comment_link_file_path = '/Users/Vidya_Thesis/data/posts_input.xml'
    n = 100000
    qa_object_list = []

    contextWords = []
    i = 0
    
    #reading the input file
    for attr_dic in xmliter(xml_comment_link_file_path, 'row'):

        post_id = int(attr_dic['@Id'])
        post_type_id = int(attr_dic['@PostTypeId'])

        if post_type_id == 2:
            parent_id = int(attr_dic['@ParentId'])
            post_id = parent_id  # answers to the particular question ID

        body = (attr_dic["@Body"])
        getFormulaAndContextWords(post_id, post_type_id, body, 10, qa_object_list)
        i = i + 1
       
    # write output to a file
    output_formula_file = open('/Users/Vidya_Thesis/data/output_file.tsv', 'w')
    output_formula_file.write("ID" + delimiter + "question" + delimiter + "question_CW" + delimiter +
                              "answer" + delimiter + "answer_CW" + "\n")
    for qa in qa_object_list:
        length_of_question = 3
        question = ""
        q_cw = []
        a_cw = []
        ans = ""
       
        for item_q in qa.qList:
            question = item_q.formula
            q_cw = item_q.contextWords

        for item_a in qa.aList:
            ans = item_a.formula
            a_cw = item_a.contextWords

            string_qa = str(qa.ID) + delimiter + question + delimiter + str(q_cw) + delimiter + ans + delimiter + str(
                a_cw) + "\n"
            output_formula_file.write(string_qa)

    print("File written successfully!")
    output_formula_file.close()
