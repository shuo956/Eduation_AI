'''
Created on Nov 26, 2017
@author: Guanliang Chen
'''

import sys

import json, os, time, random, shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re

def merge_gather_data(path):
    
    data_dump = []
    
    # Gather category relation
    category_file = open(path + "category_video_relation", "r")
    category_video_map = json.loads(category_file.read())
    video_set = set()
    video_category_map = {}
    
    title_link_map = {}
    title_set = set()
     
    for category in category_video_map.keys():
        videos = category_video_map[category]
        for video in videos:
            if video["url"] not in video_set:
                video_set.add(video["url"])
                video_category_map[video["url"]] = []
            video_category_map[video["url"]].append(category)
            
            url = video["url"]
            title = video["video_title_length"]
            if title not in title_set:
                title_set.add(title)
                title_link_map[title] = []
            
            title_link_map[title].append(category)
            
    
    
    # Gather collected videos
    video_files = os.listdir(path + "ted_videos/")
    for video_file in video_files:
        video_object = json.loads(open(path + "ted_videos/" + video_file, "r").read())
        video_youtube_link = video_object["video_youtube_link"]
        
        parsed = urlparse.urlparse(video_youtube_link)
        video_youtube_id = str(urlparse.parse_qs(parsed.query)['v'][0])
        
        if os.path.exists(path + "transcripts/" + video_youtube_id):
            transcript_file = open(path + "transcripts/" + video_youtube_id)
            transcript = transcript_file.read()
            lines = transcript.split("\n")
            
            index = None
            for i in range(len(lines)):
                if lines[i] == "":
                    index = i + 1
                    break
            
            processed_transcript = ""
            for i in range(index, len(lines)):
                processed_transcript += (lines[i] + " ")
            # processed_transcript = processed_transcript.lower().strip()
            
            video_object["transcript"] = processed_transcript
            if video_object["video_title_length"] in title_link_map.keys():
                video_object["categories"] = title_link_map[video_object["video_title_length"]]
            else:
                video_object["categories"] = []
            
            if "quizzes" in video_object.keys():
                data_dump.append(video_object)
    
    out_file = open(path + "data_dump", "w")
    out_file.write(json.dumps(data_dump))
    out_file.close()
 


def collect_category_relation(path):    
    driver = webdriver.Chrome(executable_path='../chromedriver')
    driver.maximize_window()
    
    home_link = "https://ed.ted.com/lessons"
    category_tuples = []
    
    driver.get(home_link)
    
    # Click "log in"
    click_action(driver, "//a[@href='/session']")
    
    # Log in
    driver.find_element_by_xpath("//input[@data-testid='lookup__username__1']").send_keys('username')
    click_action(driver, "//button[@data-testid='lookup__continue__3']")

    driver.find_element_by_xpath("//input[@data-testid='credentials__password__2']").send_keys('password')
    click_action(driver, "//button[@data-testid='credentials__continue__3']")
    
    # Gather subject categories
    xml_categories = driver.find_elements_by_xpath("//a[@class='tdd-dropdown__link tdd-dropdown__link--strong']")

    for xml_category in xml_categories:

        category_link = xml_category.get_attribute('href')
        category=category_link.split('=')[1]
        category_tuples.append([category, category_link])

    category_videos_map = {}
        
    for category_tuple in category_tuples:
        category = category_tuple[0]
        category_link = category_tuple[1]
        
        category_videos_map[category] = []        
               
        # Click a subject category and gather the number of total pages
        driver.get(category_link)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #time.sleep(3)
        try:
           # driver.find_element_by_xpath("//li[@class='last next']/a").click()
            total_pages = driver.find_elements_by_xpath("//a[@class='tdd-pgn__link']")
            total_pages=total_pages[-1].get_attribute('href')
            page_ref='='.join(total_pages.split('=')[:-1])
            total_pages=int(total_pages.split('=')[2])
            total_pages = int(total_pages)
        except:
            total_pages = 1
        
        for i in range(1, total_pages + 1):            
            video_group_link = page_ref + "=" + str(i)
            driver.get(video_group_link)
                        
            videos = driver.find_elements_by_xpath("//a[@class='tdd-lcard__image']")
            times=driver.find_elements_by_xpath("//span[@class='tdd-lcard__time']")

            for index,video in enumerate(videos):
                url = video.get_attribute('href')
                temp_url=url[18:]
                names=driver.find_elements_by_xpath("//a[@href='{}']".format(temp_url))

                names=names[-1].get_attribute('innerHTML')

                time=times[index].get_attribute('innerHTML')

                video_title_length =names+' - '+str(time)

                category_videos_map[category].append({"video_title_length":video_title_length, "url":url})

                
    out_file = open(path + "category_video_relation", "w")
    out_file.write(json.dumps(category_videos_map))
    out_file.close()


def click_action(driver, xpath):
    element = driver.find_element_by_xpath(xpath)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    

def collect_data(path):
    driver = webdriver.Chrome(executable_path='../chromedriver')
    home_link = "https://ed.ted.com/lessons"
    driver.get(home_link)

    # Click "log in"
    click_action(driver, "//a[@href='/session']")

    # Log in
    driver.find_element_by_xpath("//input[@data-testid='lookup__username__1']").send_keys('shua0043@gmail.com')
    click_action(driver, "//button[@data-testid='lookup__continue__3']")

    driver.find_element_by_xpath("//input[@data-testid='credentials__password__2']").send_keys('sh061217')
    click_action(driver, "//button[@data-testid='credentials__continue__3']")

    # Gather collected video list

    collected_videos = set()
    if not os.path.isdir(path + "videos/"):
       os.mkdir( path+ 'videos/')
    video_files = os.listdir(path+'videos/')
    for video_file in video_files:
        if video_file != ".DS_Store":
            collected_videos.add(json.loads(open(path + "videos/" + video_file,"r").read())["video_title_length"])
    #video='/home/shuo/Documents/AI_learning/LearningQ/data/teded/teded_crawled_data/category_video_relation'
    #a=json.loads(open(video, "r").read())
    #print(a)
    #collected_videos.add(a["video_title_length"])
    print("There are %d collected videos." % len(collected_videos))
    total_pages = driver.find_elements_by_xpath("//a[@class='tdd-pgn__link']")
    total_pages = total_pages[-1].get_attribute('href')
    page_ref = '='.join(total_pages.split('=')[:-1])
    total_pages = int(total_pages.split('=')[-1])
    total_pages = int(total_pages)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   # time.sleep(3)
   # driver.find_element_by_xpath("//li[@class='last next']/a").click()
   # total_pages = driver.find_element_by_xpath("//li[@class='page active']").text
   # total_pages = int(total_pages)
    x=True
    for i in range(1, total_pages+1):
        video_group_link = home_link + "?page=" + str(i)
        driver.get(video_group_link)
        f=open('r.txt','w')

        videos = driver.find_elements_by_xpath("//a[@class='tdd-lcard__image']")
        times = driver.find_elements_by_xpath("//span[@class='tdd-lcard__time']")

        video_tuples = []
        for index,video in enumerate(videos):
            url = video.get_attribute('href')
            temp_url = url[18:]
            names = driver.find_elements_by_xpath("//a[@href='{}']".format(temp_url))

            names = names[-1].get_attribute('innerHTML')

            r_time = times[index].get_attribute('innerHTML')

            video_title_length = names + ' - ' + str(r_time)
            video_tuples.append([url, video_title_length])

        for tuple in video_tuples:
            video_link = tuple[0]
            video_title_length = tuple[1]
            try:
                if video_title_length in collected_videos:
                    continue
                video_json_object = {"video_link":video_link, "video_title_length":video_title_length}

                driver.get(video_link)
                video_description = driver.find_element_by_xpath("//div[@class='lessonDescription']").get_attribute('innerHTML')
                video_json_object["video_description"] = video_description.strip()
                # Click the "Think" button
                try:
                    # For some videos, there is no quiz questions
                    time.sleep(0.5)
                    driver.find_element_by_xpath("//a[@id='think-link']")
                    click_action(driver, "//a[@id='think-link']")

                except:
                    # Locate the video
                    video_iframe = driver.find_element_by_xpath("//iframe[@id='playerContainer']")
                    driver.switch_to.frame(video_iframe)
                    video_youtube_link = driver.find_element_by_xpath("//a[@class='ytp-watermark yt-uix-sessionlink']").get_attribute('href')
                    video_json_object["video_youtube_link"] = video_youtube_link
                    out_file = open(path + "videos/" + video_title_length, "w")
                    out_file.write(json.dumps(video_json_object))
                    out_file.close()
                    continue

                # Locate the quizzes
                num_quiz_divs = 0
                while num_quiz_divs == 0:
                    quiz_divs = driver.find_elements_by_xpath("//div[@data-position]")
                    print(7)
                    time.sleep(0.5)

                    num_quiz_divs = len(quiz_divs)
                quizzes = []
                print(num_quiz_divs)
                f=open('w.txt','w')
                ele=driver.page_source
                f.write(ele)
                f.close()
                for j in range(num_quiz_divs):
                    # Loop over quizzes
                    driver.get(video_link + "/review_open#question-" + str(j+1))
                    time.sleep(0.5)
                    driver.get(video_link + "/review_open#question-" + str(j+1))
                    print(video_link + "/review_open#question-" + str(j+1))
                    time.sleep(0.5)

                    open_question_mark = None
                    try:
                        driver.find_element_by_xpath("//div[@data-position=" + str(j) + "]//div[@class='panel-response']")
                        time.sleep(0.5)

                        open_question_mark = True
                    except:

                        open_question_mark = False

                    # Quizzes
                    quiz_description = None
                    quiz_options = []

                    if open_question_mark:
                        # For open-ended questions
                        # Mouse hover
                        element = driver.find_element_by_xpath("//div[@data-position=" + str(j)+ "]//div[@class='panel-response']")
                        hover = ActionChains(driver).move_to_element(element)
                        hover.perform()
                        if x:
                            f=open('open_question','w')
                            f.write(driver.page_source)
                            f.close()
                            x=False
                        quiz_description = driver.find_element_by_xpath("//div[@data-position=" + str(j)+ "]//div[@class='panel-response']/div/h5").text
                        print(quiz_description)
                        quizzes.append({"quiz_description": quiz_description, "question_type":"open-ended"})
                    else:
                        # For multiple-choices questions

                        # Mouse hover
                        element = driver.find_element_by_xpath("(//div[@class='question scrollable text-ultralight'])[1]")
                        hover = ActionChains(driver).move_to_element(element)
                        hover.perform()
                        sleep(0.5)
                        # Collect textual information
                        driver.get(video_link + "/review_open#question-" + str(j + 1))

                        quiz_text = driver.find_element_by_xpath("(//div[@class='question scrollable text-ultralight'])")
                        print(j)
                        print(quiz_text)
                        lines = quiz_text.split("\n")
                        lines=[item for item in lines if item !='']
                        quiz_description = lines[0]
                        for x in range(1,len(lines),2):
                            letter_id = lines[x]
                            numerical_id = x/2
                            option = lines[x+1]
                            quiz_options.append({"letter_id":letter_id, "option_text":option, "numerical_id":numerical_id})
                        #print(quiz_options)
                        # Collect answer & hint
                        hint_mark = False
                        answer_mark = False

                        correct_answer_id = None
                        hint = None

                        num_options = len(quiz_options)

                        for k in range(num_options):
                            driver.get(video_link + "/review_open#question-" + str(j+1))
                            time.sleep(0.5)
                            driver.get(video_link + "/review_open#question-" + str(j+1))
                            time.sleep(0.5)

                            # Mouse hover
                            #try:
                            #    try:
                            #        element = driver.find_element_by_xpath("//div[@class='clearfix a answer tried tracked'][1]")
                            #        hover = ActionChains(driver).move_to_element(element)
                            #        hover.perform()
                            #        time.sleep(0.5)
                            #
                            #        # Select answer
                            #        driver.find_element_by_xpath("(//div[@class='clearfix a answer tried tracked'])[1]").click()
                            #        # Click "Save my answer"
                            #        driver.find_element_by_xpath("(//button[@class='check'])[" + str(k + 1) + "]").click()
                            #        time.sleep(0.5)
                            #    except:
                            #        element = driver.find_element_by_xpath("//div[@class='clearfix a answer tracked correct selected'][1]")
                            #        hover = ActionChains(driver).move_to_element(element)
                            #        hover.perform()
                            #        time.sleep(0.5)
                            #
                            #        # Select answer
                            #        driver.find_element_by_xpath("(//div[@class='clearfix a answer tracked correct selected'])[1]").click()
                            #        # Click "Save my answer"
                            #        driver.find_element_by_xpath(
                            #            "(//button[@class='check'])[" + str(k + 1) + "]").click()
                            #        time.sleep(0.5)
                            #except:
                            element = driver.find_element_by_xpath("//div[@class='clearfix a answer'][1]")
                            hover = ActionChains(driver).move_to_element(element)
                            hover.perform()
                            time.sleep(0.5)
                            # Select answer
                            driver.find_element_by_xpath("(//div[@class='clearfix a answer'])").click()
                            # Click "Save my answer"
                            driver.find_element_by_xpath("(//button[@class='check'])[" + str(k + 1) + "]").click()
                            time.sleep(0.5)


                            msg_mark = False
                            while not msg_mark:
                                try:
                                    msg_text = driver.find_element_by_xpath("//div[@class='g']").text
                                    msg_mark = True
                                except:
                                    time.sleep(0.5)

                            if msg_text == "Correct!":
                                correct_answer_id = k
                                answer_mark = True
                                print("correct answer %d" % correct_answer_id)

                            if not hint_mark and "That wasn" in msg_text:
                                hint = driver.find_element_by_xpath("//button[@class='btnWhite vid']").get_attribute(
                                    'data-seconds')
                                hint_mark = True
                                # print("hint is %s" % hint)
                            if hint_mark and answer_mark:
                                break


                      #  print(1)
                        quizzes.append({"quiz_description": quiz_description, "question_type": "multiple-choices",
                                        "quiz_options": quiz_options, "hint": hint, "answer": correct_answer_id})

                    video_json_object["quizzes"] = quizzes

                   # try:
                   #     if quizzes[0]['quiz_description']==quizzes[1]['quiz_description']:
                   #         print(quizzes)
                   # except:
                   #     raise
                        # Locate the video
                        #print(2)

                    video_iframe = driver.find_element_by_xpath("//iframe[@id='playerContainer']")
                        #print(3)
                    driver.switch_to.frame(video_iframe)
                   # xxxx=open('exmaple.txt','w')
                   # xxxx.write(driver.page_source)
                    #xxxx.close()
                        #print(driver.page_source)
                    video_youtube_link = driver.find_element_by_xpath(
                            "//a[@class='ytp-title-link yt-uix-sessionlink']").get_attribute('href')
                       # print(5)
                    video_json_object["video_youtube_link"] = video_youtube_link

                    out_file = open(path + "videos/" + video_title_length, "w")
                    out_file.write(json.dumps(video_json_object))
                    out_file.close()

                    collected_videos.add(video_title_length)
            except:
                print("Failed for %s" % video_title_length)
                pass


def main():
    data_path = '../../data/teded/xxxxxx/'
    
    # Step 1: collect video-category information
   # collect_category_relation(data_path)
    
    # Step 2: collect questions
    collect_data(data_path)
    
   
if __name__ == "__main__":
    main()
    print("Done.")
    
        
    