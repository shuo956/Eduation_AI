from nltk import word_tokenize
from textblob import TextBlob
import nltk
import glob
import json
from nltk.corpus import wordnet as wn
import os
from nltk.corpus import opinion_lexicon
#get opinion lexion from nltk
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()
Positive_list=opinion_lexicon.positive()
Negative_list=opinion_lexicon.negative()
main_aspects=['Design','Content','Assessment','Interaction','Instructor']
#get feaure list for tasks
FeatureList=[]
FeatureDicts={}
aspect=open('/home/shuo/PycharmProjects/orientation_word/aspect-keywords (1).csv','r')
aspect=aspect.read()
aspect = aspect.split('\n')[1:]
aspect = [item.strip('\t"') for item in aspect]
aspect = [item.split(',') for item in aspect]

for line in aspect:
    FeatureList.extend(line)
FeatureList = [w.strip(' "') for w in FeatureList]
for i in range(len(aspect)):
    temp=[w.strip(' "') for w in aspect[i]]
    aspect[i]=temp

def change_pural(review, FeatureList):
    temp_review = review.split(' ')

    for feat in FeatureList:
        for i in range(len(temp_review)):
            if feat in temp_review[i]:
                temp_review[i] = feat

    return ' '.join(temp_review)

fileList =glob.glob('/home/shuo/PycharmProjects/orientation_word/forUse/courseReview/*')
course_list=os.listdir('/home/shuo/PycharmProjects/orientation_word/forUse/courseReview/')
FeatureDicts={}
FeatureAdjectiveDictionary={}
for p in FeatureList:
    FeatureDicts[p.lower()]=0

##implement Butclause
def ButClauseRule(Words, feature):
    for ow in Words.keys():
        if Words[ow] > Words['but']:
            if ow in Positive_list:
                Orientation = -1
            elif ow in Negative_list:
                Orientation = 1
            else:
                Orientation = 0
    return Orientation


def change_pural(review):
    wnl = WordNetLemmatizer()

    review = review.lower()
    temp_token = word_tokenize(review)
    token_tag = nltk.pos_tag(temp_token)
    temp = []
    for i in range(len(token_tag)):
        if token_tag[i][1] == 'NNS':
            single = wnl.lemmatize(token_tag[i][0], 'n')
            temp.append(single)
        else:
            temp.append(token_tag[i][0])

    return ' '.join(temp)

def deal_with_not(ow,Words,op):
    if op=='pos':
        if 'not' in Words.keys() and Words[ow] == Words['not'] + 1 or 'too' in Words.keys() and Words[ow] == Words['too'] + 1:
            Orientation = -1
        else:
            Orientation = 1
        return Orientation
    elif op=='neg':
        if 'not' in Words.keys() and Words[ow] == Words['not'] + 1 or 'too' in Words.keys() and Words[ow] == Words['too'] + 1:
            Orientation = 1
        else:
            Orientation = -1
        return Orientation
def collect_score_aspect(FeatureDicts,Feature_sent_count,aspect=aspect):
    score_dicts={}
    for item in aspect:
        score=0
        num_sent=0
        for s in item:
            score=FeatureDicts[s.lower()]
            num_sent=Feature_sent_count[s.lower()]
            if num_sent==0:
                score_dicts[s.lower()]=[0,0]
            else:
                score_dicts[s.lower()]=[score,num_sent]
    return score_dicts
for filename in course_list:
    try:
        file_path='/home/shuo/PycharmProjects/orientation_word/forUse/courseReview/'+filename
        f = json.load(open(file_path, 'r'))
        output='/home/shuo/PycharmProjects/orientation_word/forUse/courseReviewScore_with_id/'+filename
        temp_score=[]
        outfile=open(output,'w')
        for review in f:
            FeatureDicts = {}
            FeatureAdjDict = {}
            AdjDictionary = {}
            Feature_sent_count={}
            for p in FeatureList:
                FeatureDicts[p.lower()] = 0
            for p in FeatureList:
                Feature_sent_count[p.lower()] = 0
            temp_review = review['reviewBody']
            sent_list=temp_review.split(',')
            if len(sent_list)==0:
                continue
            for sent in sent_list:
                sent = change_pural(sent, FeatureList)
                Words={}
                tokens=word_tokenize(sent)
                i=0
                for t in tokens:
                    Words[t.lower()]=i
                    i+=1
                tb = TextBlob(sent)
                PossibleFeatures=[]
                postags = tb.tags
                for t in postags:
                    if t[1][0] == 'N':
                        PossibleFeatures.append(t[0].lower())
                for feature in PossibleFeatures:
                    if feature in FeatureList:
                        Orientation=0
                        if feature not in FeatureDicts.keys():
                            FeatureDicts[feature] = Orientation
                        token=word_tokenize(feature)
                        if "but" in Words.keys():
                            if Words['but']<Words[token[0]]:
                                Orientation=ButClauseRule(Words,token[0])
                            else:
                                del Words['but']
                        for ow in Words:
                            if ow not in token:



                                if ow in Positive_list:
                                    op='pos'
                                    Orientation=deal_with_not(ow,Words,op)
                                elif ow in Negative_list:
                                    op = 'neg'
                                    Orientation = deal_with_not(ow, Words, op)
                                x=len(token)
                                Distance=Words[ow]-Words[(token[x-1])]
                                Orientation = (Orientation/(abs(Distance)*1.00))
                                FeatureDicts[feature] += Orientation
                        Feature_sent_count[feature]+=1
                        tb = TextBlob(feature)
                        posfeature = tb.tags
                        for t in posfeature:
                            if t[1][0] == 'J':
                                if feature in AdjDictionary.keys():
                                    AdjDictionary[feature] += Orientation
                                else:
                                    AdjDictionary[feature] = Orientation
                            else:
                                for ow in Words.keys():
                                    tb = TextBlob(ow)
                                    postag = tb.tags
                                    for t in postag:
                                        if t[1][0] == 'J':
                                            FeatureAdjective = [feature, t[0]]
                                            if (feature, t[0]) in FeatureAdjectiveDictionary.keys():
                                                FeatureAdjectiveDictionary[(feature, t[0])] += [Orientation, Orientation]
                                            else:
                                                FeatureAdjectiveDictionary[(feature, t[0])] = [0, 0]

                            # Context dependent opinion words handling
                            if FeatureDicts[feature] == 0:
                                tb = TextBlob(feature)
                                posfeature = tb.tags
                                for t in posfeature:
                                    if t[1][0] == 'J':
                                        FeatureDicts[feature] = AdjDictionary[feature]
                                    else:
                                        for i in wn.synsets(ow):
                                            for j in i.lemmas():
                                                if j.name() in Positive_list:
                                                    FeatureDicts[feature] = 1
                                                elif j.name() in Negative_list:
                                                    FeatureDicts[feature] = -1
                                                    for k in j.antonyms():
                                                        if k.name() in Positive_list:
                                                            FeatureDicts[feature] = -1

                                                        elif k.name() in Negative_list:
                                                            FeatureDicts[feature] = 1



            score_dicts=collect_score_aspect(FeatureDicts,Feature_sent_count)
            score_dicts['rating']=review['rating']
            score_dicts['review_body']=review['reviewBody']
            score_dicts['course_id']=filename
            temp_score.append(score_dicts)

        outfile.write(json.dumps(temp_score))
        outfile.close()
    except:
        print(filename)
        print(review)
        print(sent)

