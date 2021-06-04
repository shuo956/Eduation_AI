import os
import json
from score_analyzer import collect_aspect,score_analyzer
from scipy.stats import ks_2samp
import numpy as np
import pandas as pd
np.random.seed(123456)

root_path='/home/shuo/PycharmProjects/orientation_word/forUse/course_sub/'
sub_folder=os.listdir(root_path)
aspect=open('/home/shuo/PycharmProjects/orientation_word/aspect-keywords (1).csv','r')
aspect=aspect.read()
aspect = aspect.split('\n')[1:]
aspect = [item.strip('\t"') for item in aspect]
aspect = [item.split(',') for item in aspect]

main_aspects=['Design','Content','Assessment','Interaction','Instructor']
def gather_data(file_sub,output_file):
    root_path='/home/shuo/PycharmProjects/orientation_word/forUse/course_sub/'
    f_list = os.listdir(root_path + file_sub)
    temp=[]
    for f in f_list:
        print(f)
        file_path=root_path+file_sub+'/'+f
        file_review=json.load(open(file_path,'r'))
        file_review=collect_aspect(file_review)
        temp.extend(file_review)
    output_file=open(output_file,'w')
    output_file.write(json.dumps(temp))
    a=score_analyzer()
    print(file_sub)
    print(len(temp))

    a.analyze_zero_score_only_list(temp)
    a.analyze_with_score_only_list(temp)

def analyse_data(file_path):
    review_file=json.load(open(file_path,'r'))
    a=score_analyzer()
    review_senti=a.analyze_with_score_only_list(review_file)
    review_zero=a.analyze_zero_score_only_list(review_file)
    #print(len(review_senti))
    return review_senti,review_zero
    #print(review_senti)
#outputfile = '/home/shuo/PycharmProjects/orientation_word/forUse/integrated_sub_review/{}.json'.format(sub_folder[0])
#analyse_data(outputfile)

#temp_list = []
#temp_list_zero=[]
#same_dis={}
#same_dis['sub']=[]
#same_dis['senti']=[]
#same_dis['zero_senti']=[]
#same_dis['stats']=[]
temp_df=[]
for sub in sub_folder:
    outputfile = '/home/shuo/PycharmProjects/orientation_word/forUse/integrated_sub_review_with_content/{}.json'.format(sub)
    #gather_data(sub,outputfile)
    xxx=analyse_data(outputfile)
    with_review=xxx[0]
    with_review_tab=pd.DataFrame(with_review)
    temp_col=[sub]*len(with_review)
    with_review_tab['subject']=temp_col
    temp_df.append(with_review_tab)
new_frame=pd.concat(temp_df,ignore_index=True)
print(len(new_frame))
new_frame.to_csv('summary_review_content.csv')
#frame_to_work=pd.read_csv('summary_review_unmean.csv')
#print(frame_to_work)