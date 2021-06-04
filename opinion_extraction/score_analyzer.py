import json
import numpy as np
aspect=open('/home/shuo/PycharmProjects/orientation_word/aspect-keywords (1).csv','r')
aspect=aspect.read()
aspect = aspect.split('\n')[1:]
aspect = [item.strip('\t"') for item in aspect]
aspect = [item.split(',') for item in aspect]
main_aspects=['Design','Content','Assessment','Interaction','Instructor']

import pandas as pd
for i in range(len(aspect)):
    temp=[w.strip(' "') for w in aspect[i]]
    aspect[i]=temp
def collect_aspect(course_dicts,aspect=aspect,ave=True):
    temp_list=[]
    for review in course_dicts:
        score_dicts={}
        for item in aspect:
            score=0
            num_sent=0

            for s in item:

                print(s)
                print(review[s.lower()])
                score+=review[s.lower()][0]
                num_sent+=review[s.lower()][1]
            if num_sent==0:
                score_dicts[item[0]]=0
            else:
                if ave:
                    score_dicts[item[0]]=score/num_sent
                else:
                    score_dicts[item[0]]=score

        score_dicts['rating']=review['rating']
        score_dicts['review_body']=review['review_body']
        score_dicts['course_id']=review['course_id']
        temp_list.append(score_dicts)
    return temp_list
class score_analyzer():
    def __init__(self):
        self.aspect=['']
        pass
    def analyze_zero_score(self,course_dicts_path):
        course_dicts=json.load(open(course_dicts_path,'r'))
        aspected_review=collect_aspect(course_dicts)
        temp = {}
        temp['rating'] = []
        temp['review_body']=[]
        temp['course_id']=[]
        for item in aspected_review:
            if item[main_aspects[0]]==0 and item[main_aspects[1]]==0 and item[main_aspects[2]]==0 and item[main_aspects[3]]==0 and item[main_aspects[4]]==0:
                temp['rating'].append(item['rating'])
                temp['review_body'].append(item['review_body'])
                temp['course_id'].appned(item['course_id'])
        temp['rating']=[int(item) for item in temp['rating']]

        zero_rating=pd.DataFrame(temp)
        print(len(zero_rating))
        print(zero_rating.mean())
        print(zero_rating.std())

    def analyze_with_score(self,course_dicts_path):
        course_dicts=json.load(open(course_dicts_path,'r'))
        aspected_review=collect_aspect(course_dicts)
        temp = []

        for item in aspected_review:
            if item[main_aspects[0]]==0 and item[main_aspects[1]]==0 and item[main_aspects[2]]==0 and item[main_aspects[3]]==0 and item[main_aspects[4]]==0:
                continue
            else:
                temp.append(item)
        temp_dict_non={}
        temp_dict_non['review_body']=[]
        temp_dict_non['course_id']=[]
        for sub in main_aspects:
            temp_dict_non[sub]=[]
        temp_dict_non['rating']=[]
        for item in temp:
            for cat in main_aspects:
                temp_dict_non[cat].append(item[cat])
            temp_dict_non['review_body'].append(item['review_body'])
            temp_dict_non['course_id'].append(item['course_id'])
            temp_dict_non['rating'].append(int(item['rating']))
        with_rating=pd.DataFrame(temp_dict_non)
        print(len(with_rating))
        print(with_rating.mean())
        print(with_rating.std())
    def analyze_with_score_only_list(self,aspected_review):
        temp = []

        for item in aspected_review:
            if item[main_aspects[0]]==0 and item[main_aspects[1]]==0 and item[main_aspects[2]]==0 and item[main_aspects[3]]==0 and item[main_aspects[4]]==0:
                continue
            else:
                temp.append(item)
        temp_dict_non={}
        temp_dict_non['review_body']=[]
        temp_dict_non['course_id']=[]
        for sub in main_aspects:
            temp_dict_non[sub]=[]
        temp_dict_non['rating']=[]
        for item in temp:
            for cat in main_aspects:
                temp_dict_non[cat].append(item[cat])
            temp_dict_non['rating'].append(int(item['rating']))
            temp_dict_non['review_body'].append(item['review_body'])
            temp_dict_non['course_id'].append(item['course_id'])
        with_rating=pd.DataFrame(temp_dict_non)
        #print(len(with_rating))
        #print(with_rating.mean())
        #print(with_rating.std())
        return with_rating
    def analyze_zero_score_only_list(self,aspected_review):

        temp = {}
        temp['rating'] = []
        temp['review_body']=[]
        temp['course_id']=[]
        for item in aspected_review:
            if item[main_aspects[0]]==0 and item[main_aspects[1]]==0 and item[main_aspects[2]]==0 and item[main_aspects[3]]==0 and item[main_aspects[4]]==0:
                temp['rating'].append(item['rating'])
                temp['review_body'].append(item['review_body'])
                temp['course_id'].append(item['course_id'])
        temp['rating']=[int(item) for item in temp['rating']]
        zero_rating=pd.DataFrame(temp)
        #print(len(zero_rating))
        #print(zero_rating.mean())
        #print(zero_rating.std())
        return zero_rating
#a=score_analyzer()
#path='/home/shuo/PycharmProjects/orientation_word/forUse/courseReviewScore_unmean/4319.json'
#a.analyze_zero_score(path)

