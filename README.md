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
