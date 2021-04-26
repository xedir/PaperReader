from catalogue import create
import spacy
from spacy.matcher import Matcher, PhraseMatcher
import os
import preprocessing
from datetime import datetime
import pandas as pd

#load nlp pipeline
nlp = spacy.load('en_core_web_lg')

class Match(object):
    hit_phrase = ''
    hit_counter = ''
    hit_category = ''
    paper=''

    def __init__(self, phrase, counter, category, paper):
        self.hit_phrase = phrase
        self.hit_counter = counter
        self.hit_category = category
        self.paper = paper

    def __str__(self):
        return '[Phrase: ' + self.hit_phrase + ", Frequency: " + str(self.hit_counter) + ", Category: " + self.hit_category + ', '+ self.paper+"]"

    def __repr__(self):
        return '[Phrase: ' + self.hit_phrase + ", Frequency: " + str(self.hit_counter) + ", Category: " + self.hit_category+ ', '+ self.paper+"]"

def getPhrasesHardcoded():
    # Define keyword lists / hardcoded, new version in getPhrases()

    disaster_list = ["Disaster Phrases",'disaster', 'crisis','MCI','mass casualty incident','mass-casualty incident', 'accident','disease','earthquake','epidemic','fire','flood','flooding','gradual onset','hurricane','pandemic','quick onset','quick-onset','rapid onset','rapid-onset', 'short-notice','slow onset','slow-onset','slower onset','storm','tidal wave','tornado','tsunami','typhoon','wildfire', 'hazard', 'multihazard','snowstorm', 'blizzard', 'rain', 'snow']

    phase_list = ["Phase Phrases",'mitigation','mitigate','recover','recovery','preparedness','readiness','responce','response','respond','prepare']

    problem_list = ["Problem Phrases",'cooperation','volunteer','behaviour','behavior','housing','locate','inventory', 'relief distribution','evacuation','procurement','allocate','allocation','coordinate','coordination','evacuate','manufacture','market allocation','material handling','personal transport','personal transportation','procure','procurement process','resource allocation','resource distribution','risk analysis','risk assessment','risk management','risk','training','transport','transportation',
 'warehouse work','warehousing', 'capacity','staff', 'information collection','information sharing', 'relief supplies', 'communication', 'infrastructure', 'resilience', 'community', 'fleet management']

    method_list = ["Method Phrases",'algorithm','heuristic','Bayesian','optimize','optimise','optimisation','optimization', "approximate", "approximation"]

    simulation_outcome_list = ["Simulation Outcome Phrases",'simulation experiment','simulator','simulation model','simulation tool','computer simulation','computational model','complex simulation','simulation framework','simulated reality','approximate solution', "scenario analysis", "best-case scenario", "worst-case scenario", "sensitivity analysis", "performance measurement"]
  
    simulation_method_list = ["Simulation Method Phrases",'Monte Carlo','Monte-Carlo','Agent-based','Agent based','Multi agent','Multi-agent','System Dynamic','System-Dynamic','Discrete Event','Discrete-Event', "traffic simulation"]

    count_list = ["Simulation Count Phrases","simulation", "simulate"] 

    phrases = [disaster_list,phase_list, problem_list, method_list, simulation_outcome_list, simulation_method_list,count_list ]

    return phrases
    
def getPhrases():
    phrases_df = pd.read_csv("phrases.csv", encoding='utf-8', sep=";")
    phrases = []
    for column in phrases_df:
        phrases.append([column] + phrases_df[column].dropna().tolist())
    return phrases

def createPattern(word_list, matcher, name):
    # create and add patterns to matcher for individual keyword lists
    # convert the phrases into document object using nlp.make_doc to #speed up.
    patterns = [nlp(text) for text in word_list]
    # add the patterns to the matcher object without any callbacks
    matcher.add(name, None, *patterns)

def main():

    path = r"C:\Users\henke\Documents\PRpapers"
    arr = os.listdir(path)    
    results_frame = pd.DataFrame(columns=['phrase','frequency','category', 'paper'])

    # create pattern for search phrases
    phrases = getPhrases()

    # create the PhraseMatcher object and populate it
    matcher = PhraseMatcher(nlp.vocab, attr='LEMMA')
    for p in phrases:
        createPattern(p,matcher,p[0])

    #iterate through papers in arr dict.
    for paper in arr:
        if paper.endswith('.pdf'):
            
            #get pdf text for each paper
            pdf_text = preprocessing.processPDF(path, paper)

            #create spacy doc from text with nlp pipeline
            doc = nlp(pdf_text)

            print(("results for paper: " + paper).encode("utf-8"))

            # call matcher on doc and store results in matches
            matches = matcher(doc)
            #create hits list for further processing as unique hits list
            hits = []

            # populate hits list
            for match_id, start, end in matches:
                string_id = nlp.vocab.strings[match_id]  # Get string representation
                span = doc[start:end]  # The matched span
                hits.append((span.text).lower())
                #print(match_id, string_id, start, end, span.text)

            # get unique hits from complete hit list
            unique_hits = set(hits)

            # create and initialize hit_dict with unique hits to calculate frequency of each unique hit
            hit_dict={}
            for hit in unique_hits:
                hit_dict[hit] = 0


            cleaned_matches = []

            tmp_frame = pd.DataFrame(columns=['phrase','frequency','category', 'paper'])
            # calculate frequency of unique hits and store in hit_dict dictionary
            for hit in unique_hits:
                string_id=''
                counter=0

                for match_id, start, end in matches:
                    span = doc[start:end]  # The matched span
                    if ((span.text).lower() == hit):
                        hit_dict[hit] += 1
                        counter+=1
                        string_id = nlp.vocab.strings[match_id]  # Get string representation
                        text=span.text
                match = Match(text, counter, string_id, paper)
                cleaned_matches.append(match)
                tmp_frame = tmp_frame.append({'phrase': match.hit_phrase, 'frequency': match.hit_counter, 'category':match.hit_category, 'paper': match.paper}, ignore_index=True)

            results_frame = results_frame.append(tmp_frame)

    results_frame.to_csv('C:/Users/henke/Documents/results.csv')


if __name__ == "__main__":
    start = datetime.now()
    main()
    after = datetime.now()
    print("run startet at: " + start.strftime("%H:%M:%S"))
    print("run ended at: " + after.strftime("%H:%M:%S"))
    duration = after-start
    print("total runtime was: ")
    print(duration)

