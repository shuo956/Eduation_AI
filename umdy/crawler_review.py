import sys

import json, os, time, random, shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
from bs4 import BeautifulSoup
import ast
def collect_catlog():
    """
    collect category and subcategory list
    """
    webdriver_path = '/home/shuo/Documents/AI_learning/umdy/code/chromedriver'
    driver = webdriver.Chrome(executable_path=webdriver_path)
    f = open('catlog_list.txt', 'w')
    f_sub=open('subcatlog_list.txt','w')
    home_link = "https://www.udemy.com/"
    category_tuples = []

    driver.get(home_link)
    catlogs = driver.find_elements_by_xpath("//a[@class='js-side-nav-cat']")
    subcatlogs = driver.find_elements_by_xpath("//a[@class='js-side-nav-cat js-subcat']")
    # topics=driver.find_elements_by_xpath("//a[@class='js-side-nav-cat js-subcat']")
    catlist = []
    for ele in catlogs:
        temp_dic = {}
        catlog = ele.get_attribute('innerHTML')
        catlog = catlog.split(' ')
        for i in range(len(catlog)):
            if catlog[i] == '&amp;':
                catlog[i] = 'and'
        catlog = '-'.join(catlog)
        href = ele.get_attribute('href')
        data_id = ele.get_attribute('data-id')
        temp_dic['catlog'] = catlog
        temp_dic['url'] = href
        temp_dic['data-id'] = data_id
        catlist.append(temp_dic)
    f.write(json.dumps(catlist))
    subcatlist = []
    for ele in subcatlogs:
        temp_dic = {}
        subcatlog = ele.get_attribute('innerHTML')

        subcatlog = subcatlog.split(' ')
        for i in range(len(subcatlog)):
            if subcatlog[i] == '&amp;':
                subcatlog[i] = 'and'
        subcatlog = ''.join(subcatlog)
        href = ele.get_attribute('href')
        data_id = ele.get_attribute('data-id')
        temp_dic['subcatlog'] = subcatlog
        temp_dic['url'] = href
        temp_dic['data-id'] = data_id
        subcatlist.append(temp_dic)
    f_sub.write(json.dumps(subcatlist))
def get_single_sub_course(subcate_dict,driver):
    wrong_one=open('error.txt','w')
    subcate_dict_copy=subcate_dict
    page_link="https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={}&page_size=16&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&category_id={}&source_page=category_page&locale=en_US&currency=aud&navigation_locale=en_US&skip_price=true&sos=pc&fl=cat"
    data_id=int(subcate_dict['data-id'])
    driver.get(page_link.format(1,data_id))
    sub_page_source=driver.page_source
    sub_soup=BeautifulSoup(sub_page_source)
    sub_soup=sub_soup.text
    sub_source_list = json.loads(sub_soup)
    total_pages=sub_source_list['unit']['pagination']['total_page']
    subcate_dict_copy['course']=[]
    for i in range(1,total_pages+1):
        driver.get(page_link.format(i,data_id))
        page_to_crawler=driver.page_source
        if not page_to_crawler:
            continue
        page_to_crawler=BeautifulSoup(page_to_crawler)
        page_to_crawler=page_to_crawler.text
        page_to_crawler=json.loads(page_to_crawler)
        if 'unit' in page_to_crawler:
            for course in page_to_crawler['unit']['items']:
                subcate_dict_copy['course'].append(course)
        else:
            wrong_one.write(str(i)+str(subcate_dict['subcatlog'])+'\n')
            continue
    return subcate_dict_copy

def collect_course_link(sub_list):
    webdriver_path = '/home/shuo/Documents/AI_learning/umdy/code/chromedriver'
    driver = webdriver.Chrome(executable_path=webdriver_path)
    f=open(sub_list,'r')
    sub_list=json.loads(f.read())[5:]
    temp_sub=[]
    for subcate in sub_list:
        course_info = open(subcate['catlog'] + '.txt', 'w')
        sub_dict=get_single_sub_course(subcate,driver)
        course_info.write(json.dumps(sub_dict))
        print(subcate['catlog'])
        course_info.close()

def collect_courses_review(course_listpath,review_folder):
    course_list=open(course_listpath,'r')
    course_list=json.load(course_list)
    chrom_dirver = '/home/shuo/Documents/AI_learning/LearningQ/code/chromedriver'
    prefix_url = 'https://www.udemy.com'
    driver = webdriver.Chrome(executable_path=chrom_dirver)
    for course in course_list['course']:
        try:
            collect_reviews(course,driver,review_folder)
        except:
            print(course['url'])

def collect_reviews(course,driver,review_folder):

    review_path_template = 'https://www.udemy.com/api-2.0/courses/{}/reviews/?courseId={}&fields%5Bcourse_review%5D=%40default%2Cresponse%2Ccontent_html%2Ccreated_formatted_with_time_since&fields%5Bcourse_review_response%5D=%40min%2Cuser%2Ccontent_html%2Ccreated_formatted_with_time_since&fields%5Buser%5D=%40min%2Cimage_50x50%2Cinitials&is_text_review=1&ordering=course_review_score__rank%2C-created&page={}'
    i=1
    review_file=open(review_folder+'/'+course['title'].replace(' ','_')+'.txt','w')
    data_id=course['id']
    review_path=review_path_template.format(data_id,data_id,i)
    driver.get(review_path)
    review=driver.page_source
    review = BeautifulSoup(review)
    review = review.text
    review = json.loads(review)
    review_file.write(str(review)+'\n')
    try:
        while review['next'] is not None :
            i+=1
            review_path = review_path_template.format(data_id, data_id, i)
            driver.get(review_path)
            review = driver.page_source
            review = BeautifulSoup(review)
            review = review.text
            review = json.loads(review)
            review_file.write(str(review) + '\n')
        review_path = review_path_template.format(data_id, data_id, i)
        driver.get(review_path)
        review = driver.page_source
        review = BeautifulSoup(review)
        review = review.text
        review = json.loads(review)
        review_file.write(str(review) + '\n')
        review_file.close()
    except:
        print(course['url'])
#collect_catlog()
course_list='/home/shuo/Documents/AI_learning/umdy/code/Development.txt'
review_folder='/home/shuo/Documents/AI_learning/umdy/data/reviews'
cat_dir='/home/shuo/Documents/AI_learning/umdy/'
cate_list=os.listdir(cat_dir)
for cate in cate_list[4:]:
    print(cate)
    cate_path=cat_dir+cate
    collect_courses_review(course_list,review_folder)
