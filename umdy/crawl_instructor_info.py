import sys

import json, os, time, random, shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
from bs4 import BeautifulSoup

def collect_instructors_info(course_listpath,instructor_folder):
    course_list=open(course_listpath,'r')
    course_list=json.load(course_list)
    chrom_dirver = '/home/shuo/Documents/AI_learning/LearningQ/code/chromedriver'
    prefix_url = 'https://www.udemy.com'
    driver = webdriver.Chrome(executable_path=chrom_dirver)
    ins_id=[]
    for course in course_list['course']:
        try:
            for instructor in course['visible_instructors']:
                if instructor['id'] in ins_id:
                    continue
                else:
                    ins_id.append(instructor['id'])
                profix_url=prefix_url+instructor['url']
                driver.get(profix_url)
                course_source=driver.page_source
                temp_file=open(instructor_folder+'/'+instructor['display_name'].replace(' ','_')+'.txt','w')
                temp_file.write(course_source)
                temp_file.close()
                time.sleep(1)

        except:
            print(course['url'])
instructors_folder='/home/shuo/Documents/AI_learning/umdy/instructor_id'
cat_dir='/home/shuo/Documents/AI_learning/umdy/category_course/'
cate_list=os.listdir(cat_dir)
for cate in cate_list[9:]:
    cate_path=cat_dir+cate
    collect_instructors_info(cate_path,instructors_folder)