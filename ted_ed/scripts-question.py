from text_analyzer import text_analysis
import re
from transformers import BertForNextSentencePrediction, BertTokenizer,MobileBertTokenizer, MobileBertForNextSentencePrediction
from torch.nn.functional import softmax
import torch
from youtube_transcript_api import YouTubeTranscriptApi
import random
"""
this is used to map question with hint directed sentences

"""

def get_sentences(video_id):
    """
    input: video_id
    ouput: list of dictionarys, dict['sentence','seconds']
    """
    x = YouTubeTranscriptApi.get_transcript(video_id)
    temp = []
    pattern = r' *[\.\?!][\'"\)\]]* *'
    start = 0

    for i in range(len(x)):
        temp_dict = {}
        temp_text = ''
        if re.search(pattern, x[i]['text']):
            for sent in x[start:i + 1]:
                temp_text += '\n'
                temp_text += sent['text']
            temp_dict['sentence'] = temp_text.replace('\n',' ')

            temp_dict['seconds'] = int(x[start]['start'])
            temp.append(temp_dict)
            start = i + 1
    temp=[ele for ele in temp if ele['sentence']!='']
    return temp
def get_sent(dicts,hint):
    """
    get_sentences that answers the questions from list of dictionary acorrding to hint seconds
    """
    temp_sentence=''
    for item in dicts:
        if int(hint)>=item['seconds']:
            if item['sentence'].strip()!='':
                temp_sentence=item['sentence']
    return temp_sentence
def get_question_hint_sentence_x(ele):
    """
    extract candidates sentences around approximate video hint time from sentences

    """
    transcript=ele['transcript'].split('\n')
    transcript=' '.join(transcript)
    transcript= re.split(r' *[\.\?!][\'"\)\]]* *', transcript)
    word_count=0
    for item in transcript:
        word_count+=len(item.split(' '))
    transcript=[item for item in transcript if item !='']

    weight_list=[len(item.split(' '))/word_count for item in transcript]
    num_sentence=len(transcript)
    time_length=ele['length']
    seconds=int(time_length.split(':')[0])*60+int(time_length.split(':')[1])
    temp_ele={}
    temp_ele=ele
    temp_ele['question']=[]


    for question in ele['questions']:
       if 'hint' in question.keys():
           data_seconds=question['hint']
           if data_seconds=='':
               continue
           if data_seconds is None:
               continue
           locate_sentnce=int(data_seconds)/seconds
           for i in range(len(weight_list)):
               if locate_sentnce-weight_list[i]<=0:
                   break
               else:
                   locate_sentnce-=weight_list[i]

           question['responding_candidate']=[]
           try:

               question['responding_candidate'].append(transcript[i-1])
           except:
               pass
           question['responding_candidate'].append(transcript[i])
           try:
               question['responding_candidate'].append(transcript[i+1])

           except:
               pass
           try:
               question['responding_candidate'].append(transcript[i + 2])
           except:
               pass
           question['video_answer_hinted'] = transcript[i]

           temp_ele['question'].append(question)
    return temp_ele
def get_question_hint_sentence(ele):
    print(ele)
    temp_ele={}
    temp_ele=ele
    temp_ele['question']=[]
    video_id=ele['youtube_link'].split('=')[-1]
    gathered_sentences=get_sentences(video_id)
    for question in ele['questions']:
        temp_quiz=question
        if question['question_type']=='open-ended':
            continue
        if 'hint' in question.keys():
            if temp_quiz['hint']!='':

                data_seconds=temp_quiz['hint']
                if data_seconds:
                    chosen_sentence = get_sent(gathered_sentences, data_seconds)
                    temp_quiz['responding_sentence']=chosen_sentence
                    temp_ele['question'].append(temp_quiz)
    return temp_ele
def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]

def get_predicted_answer_x(tokenizer,model,ele):
    """
    calcaute probility of next sentences
    """
    temp_dic={}
    temp_dic['title']=ele['title']
    temp_dic['questions']=[]
    for i in range(len(ele['question'])):
        first_sentence=ele['question'][i]['quiz_description'].strip(' ')
        next_sentences=ele['question'][i]['responding_sentence']
        temp_q={}
        x=[]
        for sentence in next_sentences:
            encoding = tokenizer(first_sentence, sentence, return_tensors='pt')
            outputs = model(**encoding, labels=torch.LongTensor([1]))
            logits = outputs.logits
            probs=softmax(logits,dim=1)[0][0].item()
            x.append(probs)
        a=argmax(x)
        temp_q['question']=first_sentence
        temp_q['prediction']=next_sentences[a]
        temp_q['confidence']=x[a]
        temp_q['candidate']=next_sentences
        temp_dic['questions'].append(temp_q)
    return temp_dic
def get_predicted_answer(tokenizer,model,ele):
    """
    calcaute probility of next sentences
    """
    temp_dic={}
    temp_dic['title']=ele['title']
    temp_dic['question']=[]
    for i in range(len(ele['question'])):
        first_sentence=ele['question'][i]['quiz_description'].strip(' ')
        next_sentence=ele['question'][i]['responding_sentence']
        temp_q={}
        encoding = tokenizer(first_sentence, next_sentence, return_tensors='pt')
        outputs = model(**encoding, labels=torch.LongTensor([1]))
        logits = outputs.logits
        probs = softmax(logits, dim=1)[0][0].item()
        temp_q['question']=first_sentence
        temp_q['prediction']=next_sentence
        temp_q['confidence']=probs
        temp_dic['question'].append(temp_q)
    return temp_dic


def locate_document(sentence,document):
    for i in range(len(document)):

        if sentence in document[i]:
            return i
def get_candidate_set(doc,numbers):
    temp_candi=doc['transcript']
    sents=temp_candi.replace('\n',' ')
    sents = re.split(r' *[\.\?!][\'"\)\]]* *', sents)
    temp_list=[]
    for i in range(len(sents)-numbers):
        temp_sent=''
        for j in range(numbers):
            temp_sent+=sents[i+j]
        temp_list.append(temp_sent)
    return temp_list
def calculate_acc(document,model,tokenizer,numbers=2):
    ted_doc=get_question_hint_sentence_x(document)
    total_quesiton = 0
    correct_question = 0
    next_sentences = get_candidate_set(ted_doc,numbers)

    for i in range(len(ted_doc['question'])):
        total_quesiton += 1

        first_sentence = ted_doc['question'][i]['quiz_description'].strip(' ')
        located_index=locate_document(ted_doc['question'][i]['video_answer_hinted'])
        x = []
        for sentence in next_sentences:
            encoding = tokenizer(first_sentence, sentence, return_tensors='pt')
            outputs = model(**encoding, labels=torch.LongTensor([1]))
            logits = outputs.logits
            probs = softmax(logits, dim=1)[0][0].item()
            x.append(probs)
        a = argmax(x)
        if ted_doc['question'][i]['video_answer_hinted'] in next_sentences[a]:
            correct_question += 1
        # print(next_sentences)
        # print(first_sentence)
        # print(next_sentences)
        # print(new_element['question'][i]['video_answer_hinted'])
    if total_quesiton == 0:
        return False
    else:

        acc = (correct_question / total_quesiton)

        return acc

def calculate_steps(document,model,tokenizer,numbers,add_answer=False):
    ted_doc=get_question_hint_sentence_x(document)
    total_quesiton = 0
    correct_question = 0
    next_sentences = get_candidate_set(ted_doc,numbers=numbers)
    step_list=[]
    #print(next_sentences)
    for i in range(len(ted_doc['question'])):
        total_quesiton += 1

        first_sentence = ted_doc['question'][i]['quiz_description'].strip(' ')
        if add_answer:
            if get_answers(ted_doc['question'][i]):
                first_sentence=first_sentence+get_answers(ted_doc['question'][i])
        located_index=locate_document(ted_doc['question'][i]['video_answer_hinted'],next_sentences)
        x = []
        for sentence in next_sentences:
            encoding = tokenizer(first_sentence, sentence, return_tensors='pt')
            outputs = model(**encoding, labels=torch.LongTensor([1]))
            logits = outputs.logits
            probs = softmax(logits, dim=1)[0][0].item()
            x.append(probs)
        if x!=[]:
            a = argmax(x)
        else:
            return False
        if located_index is None:
            return False
        steps=a-located_index
        if steps<0:
            steps=-steps
        #print(first_sentence)
        #print(next_sentences[a])
        #print(next_sentences[located_index])
        #print(steps)
        step_list.append(steps)
        # print(next_sentences)
        # print(first_sentence)
        # print(next_sentences)
        # print(new_element['question'][i]['video_answer_hinted'])
    if total_quesiton == 0:
        return False
    else:

        return step_list
def gather_subjects(temp):
    cate_dict={}
    category=['business-economics','design-engineering-technology', 'thinking-learning', 'the-arts', 'science-technology', 'social-studies', 'health','literature-language', 'psychology',  'teaching-education', 'mathematics','philosophy-religion']
    for cate in category:
        cate_dict[cate]=[]
        for item in temp:
            if cate in temp[item]['subject']:
                cate_dict[cate].append(temp[item])
    return cate_dict
def print_stats(temp,model,tokenizer,numbers,add_answer=False):
    sec_sents=[]
    for item in temp:
        stp=calculate_steps(item,model,tokenizer,numbers,add_answer=add_answer)
        if stp:
            sec_sents.append(stp)
    print('2sents_cont amount:'+str(len(sec_sents)))
    sec_sents_numeric=[sum(item)/len(item) for item in sec_sents if item !=[]]
    ave_sec=sum(sec_sents_numeric)/len(sec_sents_numeric)
    print('average_step_for_two='+str(ave_sec))
def get_answers(question):
    if question['question_type'] == 'multiple-choices':
        for option in question['quiz_options']:
            if question['answer'] == int(option['numerical_id']):
                return option['option_text']
    return None

def main():
    path_new = '/home/shuo/Documents/AI_learning/LearningQ/data/teded/teded_crawled_data/'
    correct_path='/home/shuo/Documents/AI_learning/LearningQ/code/teded/video_hint/question_corrected.txt'
    analysis = text_analysis()
    analysis.read_relation(path_new)
    analysis.read_videoinfo(path_new)
    # questions=analysis.gather_question()
    question = analysis.video_question
    analysis.read_video_questions_from_JSON(correct_path)

    # for item in question:
    #    print(question[item]['quizzes'][0].keys())

    """
    self.video_question[title]: video_link', 'video_title_length', 'video_description', 'quizzes', 'video_youtube_link
    quizzes: quiz_description', 'question_type', 'quiz_options', 'hint', 'answer'
    multiple-choices open-ended
    """
    tokenizer = BertTokenizer.from_pretrained('bert-large-cased')
    model = BertForNextSentencePrediction.from_pretrained('bert-large-cased')
    scripts = analysis.gather_transcripts(path_new)
    temp_dic = analysis.build_question_transcripts(path_new)
    temp_dic=analysis.align_subject(temp_dic)
    cateloged=gather_subjects(temp_dic)
    stats=[]

    for c in cateloged:

        if len(cateloged[c])<=20:
            temp=cateloged[c]
        else:
            temp=random.sample(cateloged[c],10)
            print(c+'\n')
    #


        for i in range(2,5):
            print_stats(temp, model, tokenizer, i ,add_answer=False)

            break
    #f=open('b_e.txt','w')
    #for item in cateloged['business-economics']:
    #    for t in item:
    #        f.write(str(item[t])+'\n')
    #f.close()
    #temp = []
    #for item in temp_dic:
    #    for quiz in temp_dic[item]['questions']:
    #        if quiz['question_type'] == 'multiple-choices':
    #            temp.append(temp_dic[item])
    #            break
    #nn=0
    #c=0

    #temp=random.sample(temp,10)
    #sec_sents=[]
    #for item in temp:
    #    stp=calculate_steps(item,model,tokenizer)
    #    if stp:
    #        sec_sents.append(stp)
    #print('2sents_cont amount:'+str(len(sec_sents)))
    #sec_sents_numeric=[sum(item)/len(item) for item in sec_sents if item !=[]]
    #ave_sec=sum(sec_sents_numeric)/len(sec_sents_numeric)
    #print('average_step_for_two='+str(ave_sec))
    #tre_sents=[]
    #for item in temp:
    #    stp = calculate_steps(item, model, tokenizer,numbers=3)
    #    if stp:
    #        tre_sents.append(stp)
    #print('3sents_cont amount:' + str(len(tre_sents)))
    #tre_sents_numeric = [sum(item) / len(item) for item in tre_sents if item != []]
    #ave_tre = sum(tre_sents_numeric) / len(tre_sents_numeric)
    #print('average_step_for_three=' + str(ave_tre))
    #tre_sents=[]
    #for item in temp:
    #    stp = calculate_steps(item, model, tokenizer,numbers=4)
    #    if stp:
    #        tre_sents.append(stp)
    #print('3sents_cont amount:' + str(len(tre_sents)))
    #tre_sents_numeric = [sum(item) / len(item) for item in tre_sents if item != []]
    #ave_tre = sum(tre_sents_numeric) / len(tre_sents_numeric)
    #print('average_step_for_three=' + str(ave_tre))
    #tre_sents=[]
    #
    #for item in temp:
    #    stp = calculate_steps(item, model, tokenizer,numbers=5)
    #    if stp:
    #        tre_sents.append(stp)
    #print('3sents_cont amount:' + str(len(tre_sents)))
    #tre_sents_numeric = [sum(item) / len(item) for item in tre_sents if item != []]
    #ave_tre = sum(tre_sents_numeric) / len(tre_sents_numeric)
    #print('average_step_for_three=' + str(ave_tre))
        #print(new_element['title'])
        #f=open('sentence.txt','w')
        #t_l=[]
        #print(temp[0]['title'])
        #for video in temp:
        #    into_x={}
        #    new_element=get_question_hint_sentence(video)
        #    Bert_prediction= get_predicted_answer(tokenizer, model, new_element)
        #    into_x['title']=video['title']
        #    into_x['youtube_link']=video['youtube_link']
        #    into_x['questions']=[]
        #    for question in Bert_prediction['question']:
        #        if question['confidence']<0.99:
        #            temp_d={}
        #
        #            temp_d['question']=question['question']
        #            temp_d['prediction']=question['prediction']
        #            temp_d['confidence']=question['confidence']
        #            into_x['questions'].append(temp_d)
        #    if into_x['questions']!=[]:
        #        t_l.append(into_x)
        #f.write(str(t_l))
        #f.close()

if __name__=='__main__':
    main()