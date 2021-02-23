# Eduation_AI
## This project is for pretraining method for ted-ed education.
* The dataset .zip contains updated transcripts and questions from Ted-ed.
* crawler.py,get_transcripts.py are updated to crawl questions and transcripts of videos.
* text_analyzer.py are used to construct object for each video and get next sentence prediction score for questions and corrosponding candidate answer in documents.
* table_for_ted_ed.xlsx contains basic stats from ted-ed.
## Findings from ted-ed
1.Video hint with transcript not necessarily mapped to orginal sentences 
2.using next sentence prediction may not accurately find the corresponding sentences if we rank the confidence score of sentences. 
3.Video hint may not accuracte, even manually located video hint for one question may require contextual information to correctly answer questions.
