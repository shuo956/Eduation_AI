import sys
import argparse
import json, os, time, random, shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
from bs4 import BeautifulSoup
import ast


def get_subscribed_id(user_id,driver):
    sub_temp=[]
    i=1
    sub_path_template = 'https://www.udemy.com/api-2.0/users/{}/subscribed-profile-courses/?fields[course]=@default,image_50x50,image_100x100,avg_rating_recent,rating,bestseller_badge_content,badges,content_info,discount,is_recently_published,is_wishlisted,is_saved,num_published_lectures,num_reviews,num_subscribers,buyable_object_type,free_course_subscribe_url,is_in_user_subscription,learn_url,headline,instructional_level,objectives_summary,content_length_practice_test_questions,content_info_short,num_published_practice_tests,published_time,is_user_subscribed,has_closed_caption,preview_url,context_info,caption_languages&page={}&page_size=12'
    sub_path=sub_path_template.format(user_id,i)
    driver.get(sub_path)


    try:
        element = driver.find_element_by_tag_name("pre")
        element = element.get_attribute('innerHTML')
        sub_page = json.loads(element)
        for item in sub_page['results']:
            sub_temp.append(item['id'])
        if sub_page['count']>1000:
            return sub_temp
        while sub_page['next'] is not None:
            i += 1
            sub_path = sub_path_template.format(user_id, i)
            driver.get(sub_path)

            element = driver.find_element_by_tag_name("pre")
            element = element.get_attribute('innerHTML')
            sub_page = json.loads(element)
            for item in sub_page['results']:
                sub_temp.append(item['id'])
        i+=1
        sub_path = sub_path_template.format(user_id, i)
        driver.get(sub_path)
        element = driver.find_element_by_tag_name("pre")
        element = element.get_attribute('innerHTML')
        sub_page = json.loads(element)
        for item in sub_page['results']:
            sub_temp.append(item['id'])
    except:
        return sub_temp
def collect_image_user(num):
    path = '/home/shuo/user_image_{}.txt'.format(num)
    c_path = '/home/shuo/Documents/AI_learning/umdy/collected_user/collect_user_{}.txt'.format(num)
    f=open(c_path,'a')

    name_list_t=open(path,'r')
    name_list_t=name_list_t.read()
    name_list_t=json.loads(name_list_t)
    webdriver_path='/home/shuo/Documents/AI_learning/umdy/code/chromedriver'
    driver = webdriver.Chrome(executable_path=webdriver_path)
    n=0
    for user in name_list_t[5000:]:
        subscribed_course=get_subscribed_id(user[-1],driver)
        n+=1
        user.append(subscribed_course)
        f.write(json.dumps(user)+'\n')
        print(n)

if  __name__ =='__main__':
    start = time.time()
    main_arg_parser = argparse.ArgumentParser(description="non_function_generator")
    main_arg_parser.add_argument('-n', type=str, default='1', help='data_path')

    args = main_arg_parser.parse_args()
    collect_image_user(args.n)

