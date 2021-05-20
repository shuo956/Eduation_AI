import os
from bs4 import BeautifulSoup
import ast
import json
r_path='/media/shuo/Elements SE/uemdy_course/data/reviews/'
c_path="/media/shuo/Elements SE/uemdy_course/data/source_page/"
review_list=os.listdir(r_path)
course_list=os.listdir(c_path)

course_list.sort()
review_list.sort()


def collect_one_course(title):
    temp_dict = {}
    temp_dict['course_title'] = ''
    temp_dict['instructors_info'] = ''
    temp_dict['rating_info'] = ''
    temp_dict['course_id'] = ''
    temp_dict['description_info'] = ''
    temp_dict['reviews'] = ''
    temp_dict['review_content'] = ''
    temp_dict = collect_source_page_info(title, temp_dict)
    temp_dict = collect_review_context(title, temp_dict)
    return temp_dict


def collect_source_page_info(title, temp_dict):
    c_path = "/media/shuo/Elements SE/uemdy_course/data/source_page/"

    source_page = c_path + title
    source_file = open(source_page, 'r')
    source_file = source_file.read()
    source_file = BeautifulSoup(source_file)
    try:
        instructor_info = source_file.find('div', attrs={'class': 'ud-component--course-landing-page-udlite--instructors'})['data-component-props']
        instructor_info = ast.literal_eval(instructor_info)
        temp_dict['course_id'] = instructor_info['course_id']
        temp_dict['instructors_info'] = instructor_info['instructors_info']

    except:
        pass
    try:
        description_info = source_file.find('div', attrs={'class': 'ud-component--course-landing-page-udlite--description'})['data-component-props']
        description_info = ast.literal_eval(description_info)
        temp_dict['description_info'] = description_info

    except:
        pass
    try:
        rating_info = source_file.find('div', attrs={'class': 'ud-component--course-landing-page-udlite--reviews'})[
            'data-component-props']
        rating_info = json.loads(rating_info)
        temp_dict['rating_info'] = rating_info
        temp_dict['course_id'] = rating_info['course_id']


    except:
        pass
    try:
        temp_dict['course_title'] = source_file.find('title').text
    except:
        pass
    return temp_dict


def concat_review(review_path):
    f = open(review_path, 'r')
    review_list = f.read()
    review_list = review_list.split('\n')
    review_list = [item for item in review_list if item != ' ']
    temp_reviews = []
    for review in review_list[:-1]:
        res = ast.literal_eval(review)
        try:
            temp_reviews.extend(res['results'])
        except:
            return temp_reviews
    return temp_reviews


def collect_review_context(title, temp_dict):
    r_path = '/media/shuo/Elements SE/uemdy_course/data/reviews/'
    review_path = r_path + title
    reviews = concat_review(review_path)
    temp_dict['review_content'] = reviews
    return temp_dict

stats=[]
folder='/home/shuo/Documents/AI_learning/umdy/interagted_file/'
for i in range(len(course_list)):
    course_title=course_list[i]
    f=open(folder+course_title,'w')
    temp_dict=collect_one_course(course_title)
    f.write(json.dumps(temp_dict)+'\n')
    if i%10000==0:
        print(i)
    f.close()
