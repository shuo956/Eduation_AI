import json
import ast
from text_analyzer import text_analysis

def align_questions(question):
    f=open(question,'r')
    temp={}
    for item in f.readlines():
        t_dic=ast.literal_eval(item.strip('\n'))

        temp[t_dic['title']]=t_dic
    return temp
open_q='/home/shuo/Documents/AI_learning/LearningQ/code/teded/questions.txt'
t_dict=align_questions(open_q)
video_path='/home/shuo/Documents/AI_learning/LearningQ/data/teded/teded_crawled_data/'
analysis = text_analysis()
# analysis.read_realtion(path)
analysis.read_videoinfo(video_path)
# questions=analysis.gather_question()
question = analysis.video_question

# for item in question:
t=0
new_question={}
for item in t_dict:
    t += 1

    temp_question=t_dict[item]['multi']
    try:
        question_to_correct=question[item]
    except:
        continue
    #print(temp_question)
    #print(question_to_correct['quizzes'])
    question_list=[]
    open_list=[]
    for quiz in question_to_correct['quizzes']:
        if quiz['question_type']=='multiple-choices':
            question_list.append(quiz)
        else:
            open_list.append(quiz)
    print(question_list)
    if len(question_list)==0:
        continue
    if len(question_list)==len(temp_question): #check number of questions and corrected one
        pass
    else:
        print(item)
        continue
    try:
        for i in range(len(question_list)):
            question_list[i]['quiz_description']=temp_question[i]
    except:
        continue
    print('\n')

    question_list.extend(open_list)


    question[item]['quizzes']=question_list
    for q in question[item]['quizzes']:
        print(q)
    new_question[item]=question[item]

x=0
for item in new_question:
    x+=1
    print('\n')
    print(item)
    for qu in new_question[item]['quizzes']:
        print(qu)
f=open('question_corrected.txt','w')
f.write(json.dumps(new_question))
f.close()
print(x)
