from text_analyzer import text_analysis
import re
from transformers import BertForNextSentencePrediction, BertTokenizer,MobileBertTokenizer, MobileBertForNextSentencePrediction
from torch.nn.functional import softmax
import torch
from youtube_transcript_api import YouTubeTranscriptApi
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
        if int(hint)<=item['seconds']:
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


def main():
    path = '/home/shuo/Documents/AI_learning/LearningQ/data/teded/teded_crawled_data/'
    path_new = '/home/shuo/Documents/AI_learning/LearningQ/data/teded/teded_crawled_data/'

    analysis = text_analysis()
    # analysis.read_realtion(path)
    analysis.read_videoinfo(path_new)
    # questions=analysis.gather_question()
    question = analysis.video_question
    # for item in question:
    #    print(question[item]['quizzes'][0].keys())

    """
    self.video_question[title]: video_link', 'video_title_length', 'video_description', 'quizzes', 'video_youtube_link
    quizzes: quiz_description', 'question_type', 'quiz_options', 'hint', 'answer'
    multiple-choices open-ended
    """
    scripts = analysis.gather_transcripts(path)
    temp_dic = analysis.build_question_transcripts(path_new)


    temp = []
    for item in temp_dic:
        print(item)
        for quiz in temp_dic[item]['questions']:
            if quiz['question_type'] == 'multiple-choices':
                temp.append(temp_dic[item])
                break
    new_element=get_question_hint_sentence_x(temp[1])
    #for question in temp[-1]['questions']:
    #    print(question)
    #
    #print(temp[-1])
    #print(len(temp))
    tokenizer = BertTokenizer.from_pretrained('bert-large-cased')
    model = BertForNextSentencePrediction.from_pretrained('bert-large-cased')
    #tokenizer = MobileBertTokenizer.from_pretrained('google/mobilebert-uncased')
    #model = MobileBertForNextSentencePrediction.from_pretrained('google/mobilebert-uncased')
    print(temp[1])
    for i in range(len(new_element['question'])):
        first_sentence=new_element['question'][i]['quiz_description'].strip(' ')
        next_sentences=new_element['question'][i]['responding_candidate']

        x=[]
        for sentence in next_sentences:
            encoding = tokenizer(first_sentence, sentence, return_tensors='pt')
            outputs = model(**encoding, labels=torch.LongTensor([1]))
            logits = outputs.logits
            probs=softmax(logits,dim=1)[0][0].item()
            x.append(probs)
        a=argmax(x)
        #print(next_sentences)
        print(first_sentence)
        print(next_sentences)
        print(new_element['question'][i]['video_answer_hinted'])
        break
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