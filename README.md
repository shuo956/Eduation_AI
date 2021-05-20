# Eduation_AI
## This project is for pretraining method for ted-ed education.
* The dataset .zip contains updated transcripts and questions from Ted-ed.
* crawler.py,get_transcripts.py are updated to crawl questions and transcripts of videos.
* text_analyzer.py are used to construct object for each video and get next sentence prediction score for questions and corrosponding candidate answer in documents.
* table_for_ted_ed.xlsx contains basic stats from ted-ed.
## Findings from ted-ed
1.Video hint with transcript not necessarily mapped to orginal sentences.

2.using next sentence prediction may not accurately find the corresponding sentences if we rank the confidence score of sentences. 

3.Video hint may not accuracte, even manually located video hint for one question may require contextual information to correctly answer questions.

## Example question that requires extra knowledge:

You are measuring length with a meter stick. However, you do not realize that the first 4.0 centimeters of the meter stick are missing because a hungry beaver made a snack of it earlier that day. The measurements you take with the meter stick will be: 

A Accurate, but imprecise 

B  Precise, but inaccurate 

C  Imprecise and inaccurate 

D  Accurate and precise 

Video hint: Precision, on the other hand, is how consistently you can get  that result using the same method 

Predicted hint: Your accuracy improves with tools that are calibrated correctly and that you're well-trained on 

Human Judge: Both.




## Component
### Ted-ed
dataset:
1.transcripts.zip ------------------transcripts of videos
2.question_corrected.txt -------video description and question 
3.category_video_relation ------- dictionary contains category information of course
file:
1.crawler.py ------crawler file modifed for answering
2.crawler_for_question.py ------crawler for questions
3.get_all_transcripts.py ---crawler file for transcripts
4.correct_question.py ------ question aligment to answers
5.text_analyzer.py------- basic stats for transcripts and questions
6.scripts-question.py --------step calculation for located sentence to true answers
### Umdy
dataset:
1.category_course----- brief course infomration based on main subject
2.collected_user-------- try url for different user name collected from reviews.
3.course by id-----course decription,ID,average rating, distribution
4.instructor_id-------collected instructor html info contains all descriptions
5.interagted_file-----integrated info with course and instructor
file:
1.crawl_instructor_info.py----- crawl instructors
2.crawler_review.py---- crawl review by id
3.download_image.py-----user image download 
4.image_user.py---- crawl information of subcribed student
5.integrate_data.py----combine data with instructors and courses


### Opinion extraction
file:
1.text_analyzer.py ------- main implmentation of opinion score {aspects:score,rating: rating,content: content, id:id}
2.score_analyzer.py ------- reformat data to 5 aspects and informations
3.separete_course_review.py-----separated all courses into sujects
4.subject_level_mlr.py-----reformat data to csv file
dataset:
1.summary_review_content.csv -----summary opinion with orientation
2.summary_review_zero_content.csv -----summary of opinion with no orientation
