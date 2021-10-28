from QAClass import QAClass


class QuestionAnswerParser(object):

    def __init__(self, ID, post_type_id, questionList,answerList):

        self.ID = ID
        self.qList = []
        self.aList = []
        self.updateList(post_type_id, questionList, answerList)

    def updateList(self, post_type_id, QList, AList):
        if post_type_id == 1:
            for item in QList:
                self.qList.append(item)
        else:
            for item in AList:
                self.aList.append(item)

