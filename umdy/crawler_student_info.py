import sys

import json, os, time, random, shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
from bs4 import BeautifulSoup
import ast

def get_name_list(path):
    f=open(path,'r')
    name_list=f.read()
    name_list=name_list.split('\n')

    name_list=[name.replace(' ','-') for name in name_list ]
    return name_list
def get_subscribed_id(user_id,driver):
    sub_temp=[]
    i=1
    sub_path_template = 'https://www.udemy.com/api-2.0/users/{}/subscribed-profile-courses/?fields[course]=@default,image_50x50,image_100x100,avg_rating_recent,rating,bestseller_badge_content,badges,content_info,discount,is_recently_published,is_wishlisted,is_saved,num_published_lectures,num_reviews,num_subscribers,buyable_object_type,free_course_subscribe_url,is_in_user_subscription,learn_url,headline,instructional_level,objectives_summary,content_length_practice_test_questions,content_info_short,num_published_practice_tests,published_time,is_user_subscribed,has_closed_caption,preview_url,context_info,caption_languages&page={}&page_size=12'
    sub_path=sub_path_template.format(user_id,i)
    driver.get(sub_path)

    sub_page = driver.page_source
    sub_page = BeautifulSoup(sub_page)
    sub_page = sub_page.text
    sub_page = json.loads(sub_page)
    for item in sub_page['results']:
        sub_temp.append(item['id'])
    try:
        while sub_page['next'] is not None:
            i += 1
            sub_path = sub_path_template.format(user_id, i)
            driver.get(sub_path)
            sub_page = driver.page_source
            sub_page = BeautifulSoup(sub_page)
            sub_page = sub_page.text
            sub_page = json.loads(sub_page)
            for item in sub_page['results']:
                sub_temp.append(item['id'])
        i+=1
        sub_path = sub_path_template.format(user_id, i)
        driver.get(sub_path)
        sub_page = driver.page_source
        sub_page = BeautifulSoup(sub_page).text
        sub_page = json.loads(sub_page)
        for item in sub_page['results']:
            sub_temp.append(item['id'])
    except:
        return sub_temp

#def get_wishlist_id(user_id,driver):
#    wish_temp = []
#    i = 1
#    wish_path_template = 'https://www.udemy.com/api-2.0/users/{}/wishlisted-profile-courses/?fields[course]=@default,image_50x50,image_100x100,avg_rating_recent,rating,bestseller_badge_content,badges,content_info,discount,is_recently_published,is_wishlisted,is_saved,num_published_lectures,num_reviews,num_subscribers,buyable_object_type,free_course_subscribe_url,is_in_user_subscription,learn_url,headline,instructional_level,objectives_summary,content_length_practice_test_questions,content_info_short,num_published_practice_tests,published_time,is_user_subscribed,has_closed_caption,preview_url,context_info,caption_languages&page={}&page_size=12'
#    wish_path = wish_path_template.format(user_id, i)
#    driver.get(wish_path)
#
#    wish_page = driver.page_source
#    wish_page = BeautifulSoup(wish_page)
#    wish_page = wish_page.text
#    wish_page = json.loads(wish_page)
#    for item in wish_page['results']:
#        wish_temp.append(item['id'])
#    try:
#        while wish_page['next'] is not None:
#            i += 1
#            wish_path = wish_path_template.format(user_id, i)
#            driver.get(wish_path)
#            wish_page = driver.page_source
#            wish_page = BeautifulSoup(wish_page)
#            wish_page = wish_page.text
#            wish_page = json.loads(wish_page)
#            for item in wish_page['results']:
#                wish_temp.append(item['id'])
#        i += 1
#        sub_path = wish_path_template.format(user_id, i)
#        driver.get(sub_path)
#        wish_page = driver.page_source
#        wish_page = BeautifulSoup(wish_page).text
#        wish_page = json.loads(wish_page)
#        for item in wish_page['results']:
#            wish_temp.append(item['id'])
#    except:
#        return wish_temp

#def get_users_source_page(user_front_url,driver):
#    i=1
#    temp_dict={}
#    driver.get(user_front_url)
#    user_page = driver.page_source
#    user_page = BeautifulSoup(user_page)
#    user_profile = user_page.find('div', attrs={'class': 'ud-app-loader ud-component--user-profile--app ud-app-loaded'})
#    try:
#        user_profile = user_profile['data-module-args']
#        user_profile = ast.literal_eval(user_profile)['user']
#        user_id = user_profile['id']
#        user_name = user_profile['title']
#
#
#        subcribed_course_id=get_subscribed_id(user_id,driver)
#        wish_course_id=get_wishlist_id(user_id,driver)
#        temp_dict['name']=user_name
#        temp_dict['id']=user_id
#        temp_dict['subscribed']=subcribed_course_id
#        temp_dict['wishlist']=wish_course_id
#        return temp_dict
#    except:
#        return None
def collect_catlog():
    name_path='/home/shuo/Documents/AI_learning/umdy/user_name_list'
    name_list=get_name_list(name_path)
    name_list_t=name_list[:250000]
    webdriver_path='/home/shuo/Documents/AI_learning/umdy/code/chromedriver'
    driver = webdriver.Chrome(executable_path=webdriver_path)
    home_link = "https://www.udemy.com/"
    category_tuples = []
    temp=[]
    driver.get(home_link)
    time.sleep(50)
    c=0
    count_f=open('count_1.txt','w')
    f=open('user_course_info_f_1.txt','w')

    for name in name_list_t:
        name_url="https://www.udemy.com/user/"+name
        user_profile_dic=get_users_source_page(name_url,driver)
        count_f.write(str(c)+'\n')
        c+=1

        if user_profile_dic is not None:
            f.write(json.dumps(user_profile_dic) + '\n')
        for rep in range(1,10):
            try:
                user_profile_dic = get_users_source_page(name_url+'-'+str(rep), driver)
                if user_profile_dic is not None:
                    f.write(json.dumps(user_profile_dic) + '\n')

            except:
                continue
    f.close()
    count_f.close()

collect_catlog()
