import os
import shutil


root_folder='/home/shuo/PycharmProjects/orientation_word/forUse/course_sub/'
course_folder='/home/shuo/PycharmProjects/orientation_word/forUse/courseMetadata/'
course_folder_list=os.listdir(course_folder)
review_score_folder='/home/shuo/PycharmProjects/orientation_word/forUse/courseReviewScore_with_id/'
review_list=os.listdir(review_score_folder)
n=0
m=0
for cate in course_folder_list:
    sub_cate_list=os.listdir(course_folder+cate)
    os.mkdir(root_folder+cate)
    cate_folder=root_folder+cate
    print(cate_folder)
    for course in sub_cate_list:
        try:
            shutil.copy(review_score_folder+course,cate_folder)
            m+=1
        except:
            n+=1
print(n)
print(m)