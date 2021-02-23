import json
import os
import nltk
import re
from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch
import numpy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from readability import Readability

import spacy
from spacy import displacy
import en_core_web_sm
from collections import Counter
"""
code us
"""
class text_analysis:
    def __init__(self):
        self.relation=None
        self.video_question=None
        self.questions=None
        self.transcripts=None
    def read_relation(self,path):
        """
        integrate all relations into documents

        """
        relation=open(path+'category_video_relation')
        relation=json.load(relation)
        title=[]
        self.relation=relation
        for item in relation:
            for video in relation[item]:
                title.append(video['video_title_length'])
        title=list(set(title))
        new_relation=[]
        for item in title:
            tmp={}
            tmp['video_title_length']=item
            tmp['subject']=[]
            for subject in relation:
                for video in relation[subject]:
                    if video['video_title_length']==item:
                        tmp['url']=video['url']
                        tmp['subject'].append(subject)
            new_relation.append(tmp)
        self.new_relation=new_relation

        return new_relation

    def read_videoinfo(self,path):
        video_list=os.listdir(path + "videos/")

        temp={}
        for video_file in video_list:
            if video_file=='.DS_Store':
                continue
            video_jsonObject = json.loads(open(path + "videos/" + video_file, "r").read())
            temp[video_file]=video_jsonObject
        self.video_question=temp


    def gather_question(self):
        """
        questions contain all quzzies for crawled videos

        """
        questions=[]
        for item in self.video_question:
            for quiz in self.video_question[item]['quizzes']:
                questions.append(quiz['quiz_description'])
        open_ended=0
        return questions
        #for question in questions:     #question counted
        #    if question['question_type']!='open-ended':
        #        open_ended+=1
        #print(open_ended)
    def get_mintues(self):
        mins=0
        maxs=0
        for item in self.relation:
            for video in self.relation[item]:
                minutes=video['video_title_length'].split(' - ')[-1]
                minutes=int(minutes.split(':')[0])
                if minutes<mins:
                    mins=minutes
                if minutes>maxs:
                    maxs=minutes
                if minutes==0 or minutes==27:
                    print(video['video_title_length'])
                    print(video['url'])

        print(str(mins)+'-'+str(maxs))
    def gather_transcripts(self,path):
        """
        Gather all transcripts in order to collect
        :return:
        dicts[title]=transcripts
        """
        video_list=os.listdir(path+'transcripts/')
        question_list=os.listdir(path+'videos/')
        transcripts={}
        sec=0
        for i in range(len(video_list)):
            video=open(path+'transcripts/'+video_list[i],'r').read()
            video = video.split('\n')
            title=video[0]
            content=[ sent for sent in video[1:] if sent!='']
            content='\n'.join(content)

            transcripts[title]=content
            sec+=len(re.split(r'[.!?]+', content))

        self.transcripts=transcripts
  #      print(sec)
  #      i=0
  #      fin=[]
  #      k=0
  #      for title in self.transcripts:
  #          k+=1
  #          temp_title = re.sub("Title: ", '', title.split('|')[0])
  #          temp_title=temp_title.split('|')[0].strip()
  #          temp_title=re.split('-',temp_title)[0].strip(' ')
  #          temp_title=re.sub("\(version 1\)",'',temp_title)
  #          for question in question_list:
  #
  #              if temp_title.lower() in question.lower():
  #                  i+=1
  #                  fin.append(title)
  #                  break
  #          #        print(temp_title)
  #          #        print(sent)
  #      no_fin=[t for t in self.transcripts.keys() if t not in fin ]
  #      print(len(list(set(no_fin))))
  #      print(len(list(set(fin))))
  #      print(k)
  #      for item in no_fin:
  #          print(item)

        return transcripts
    def build_question_transcripts(self,path):
        question_list=os.listdir(path+'videos/')


        i=0
        fin=[]
        k=0
        temp={}

        for title in self.transcripts:
            k+=1
            temp_title = re.sub("Title: ", '', title.split('|')[0])
            temp_title=temp_title.split('|')[0].strip()
            temp_title=re.split('-',temp_title)[0].strip(' ')
            temp_title=re.sub("\(version 1\)",'',temp_title)
            for question in self.video_question:

                if temp_title.lower() in question.lower():
                    i+=1
                    fin.append(title)
                    temp[title]={}
                    temp[title]['transcript']=self.transcripts[title]
                    temp[title]['questions']=self.video_question[question]['quizzes']
                    temp[title]['length']=question.split('-')[-1]
                    temp[title]['title']=question
                    temp[title]['youtube_link']=self.video_question[question]['video_youtube_link']
               #     temp[title[]['question']=
                    break
              #        print(temp_title)
              #        print(sent)
        no_fin=[t for t in self.transcripts.keys() if t not in fin ]
        #print(len(list(set(no_fin))))
        #print(len(list(set(fin))))
        #print(k)
        #for item in no_fin:
        #    print(item)
        return temp
    def stats_scripts(self):
        """
        used to calculate unique document and maximum words for corpus

        """
        s=0
        m=0
        c=0
        for title in self.transcripts:
            word_count=len(self.transcripts[title].split(' '))
            s+=word_count
            c+=1
            n_e+=e
            if m<word_count:
                m=word_count
            if word_count==2725:
                print(title)
        print(c)
        print(s)
        print(m)

def NER(scripts,nlp):

    c=0
    for item in scripts:
        sentence=item
        prediction=nlp(sentence)
        entities=[(X.text, X.label_) for X in prediction.ents]
        number_of_entity=len(entities)
        c+=number_of_entity
    return c

def stats_scripts(scripts):
    x=0
    for item in scripts:
        doc=scripts[item].replace('\n',' ')
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', doc)
        x+=len(sentences)
    print(x)
def main():
    path='/home/shuo/Documents/AI_learning/LearningQ/data/teded/teded_crawled_data/'
    analysis=text_analysis()
    analysis.read_relation(path)
    #analysis.get_mintues()
    analysis.read_videoinfo(path)
    questions=analysis.gather_question()
    question=analysis.video_question
    #for item in question:
    #    print(question[item]['quizzes'][0].keys())
    """
    self.video_question[title]: video_link', 'video_title_length', 'video_description', 'quizzes', 'video_youtube_link
    quizzes: quiz_description', 'question_type', 'quiz_options', 'hint', 'answer'
    multiple-choices open-ended
    """
    scripts=analysis.gather_transcripts(path)
    stats_scripts(scripts)
    temp_dic=analysis.build_question_transcripts(path)

   # analysis.stats_scripts()
    temp=[]
    for item in temp_dic:
        for quiz in  temp_dic[item]['questions']:
            if quiz['question_type']=='multiple-choices':
                temp.append(temp_dic[item])
                break
    q=0
    for d in temp:
        for question in d['questions']:
            xxx=len(question['quiz_description'].split('.'))
            q+=xxx

    nlp = en_core_web_sm.load()
    #n_e=0
    total_r=0
    n=0
    for title in scripts:
        #sentences=scripts[title].split('\n')
        #e=NER(sentences,nlp)
        if len(scripts[title].split(' '))>=100:

            n+=1
            r = Readability(scripts[title])
            total_r+=r.flesch().score
        #n_e+=e
    #print(n_e)
    print(total_r)
    print(n)
    print(total_r/n)


    #print(questions)
    #analysis.stats_scripts()
    #analysis.get_mintues()
   # print(questions)
   # c=NER(questions)
   # print(c)


   # s=[]
   # for item in questions:
   #     s+=item.split(' ')
   # print(s)
   # sp = spacy.load('en_core_web_sm')
   # all_stopwords = sp.Defaults.stop_words
   # all_stopwords.remove('make')
   # text = "Nick likes to play football, however he is not too fond of tennis."
   # #split_it =word_tokenize(s)
   #
   # split_it=[word.lower() for word in s]
   # split_it = [word for word in split_it if not word in all_stopwords]
   #
   # Counters = Counter(split_it)
   #
   # # most_common() produces k frequently encountered
   # # input values and their respective counts.
   # most_occur = Counters.most_common(50)
   # for item in most_occur:
   #     print(item)

if __name__=='__main__':
    main()