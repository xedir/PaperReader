import PyPDF2
import spacy
from spacy.matcher import Matcher, PhraseMatcher
import os
import preprocessing
import most_similar
from datetime import datetime
import json
import pandas as pd


def main():

    path = r"C:\Users\henke\Documents\PRpapers"
    arr = os.listdir(path)

    # alternative keyword source
    #wordlist = most_similar.most_similar_single("supply chain")
    #print(wordlist)



    # Define keyword lists
    disaster_list = ["rapid onset", "slow onset", "fire", "wildfire", "earthquake", "epidemics", "flood", "hurricane", "typhoon", "tsunami"]
    extended_disaster_list = ['disaster', 'crisis','MCI','mass casualty incident','mass-casualty incident', 'accident','disease','earthquake','epidemic','fire','flood','flooding','gradual onset','hurricane','pandemic','quick onset','quick-onset','rapid onset','rapid-onset', 'short-notice','slow onset','slow-onset','slower onset','storm','tidal wave','tornado','tsunami','typhoon','wildfire']

    phase_list = ["mitigation", "preparedness", "response", "recovery"]
    extended_phase_list = ['mitigation','mitigate','recover','recovery','preparedness','readiness','responce','response','respond','prepare']

    problem_list = ["evacuation",'evacuate',"procurement","transportation","resource allocation","coordination","risk assessment","warehousing","training"]
    extended_problem_list = ['evacuation','procurement','allocate','allocation','coordinate','coordination','evacuate','manufacture','market allocation','material handling','personal transport','personal transportation','procure','procurement process','resource allocation','resource distribution','risk analysis','risk assessment','risk management','risk','training','transport','transportation',
 'warehouse work','warehousing', 'capacity','staff', 'information collection','information sharing']

    method_list=["algorithm","heuristic","optimization"]
    extended_method_list = ['algorithm','heuristic','Bayesian','optimize','optimise','optimisation','optimization', "approximate", "approximation"]

    simulation_outcome_list = ["simulation", "simulation model", "simulation tool", "simulation framework"]
    extended_simulation_outcome_list = ['simulator','simulation model','simulation tool','computer simulation','computational model','complex simulation','simulation framework','simulated reality','approximate solution', "scenario analysis", "best-case scenario", "worst-case scenario", "sensitivity analysis", "performance measurement"]

    simulation_method_list = ['Monte Carlo','Monte-Carlo','Agent-based','Agent based','Multi agent','Multi-agent','System Dynamic','System-Dynamic','Discrete Event','Discrete-Event', "traffic simulation"]

    simulation_count_list = ["simulation", "simulate"]  



    results_frame = pd.DataFrame(columns=['phrase','frequency','category', 'paper'])



    #iterate through papers in arr dict.
    for paper in arr:
        if paper.endswith('.pdf'):
            #get pdf text for each paper
            pdf_text = preprocessing.processPDF(path, paper)

            #load nlp pipeline
            nlp = spacy.load('en_core_web_lg')

            #nlp.add_pipe('lemmatizer')

            #create spacy doc from text with nlp pipeline
            doc = nlp(pdf_text)

            # create the PhraseMatcher object
            matcher = PhraseMatcher(nlp.vocab, attr='LEMMA')

            # create and add patterns to matcher for individual keyword lists
            # convert the phrases into document object using nlp.make_doc to #speed up.
            disaster_patterns = [nlp(text) for text in extended_disaster_list]
            # add the patterns to the matcher object without any callbacks
            matcher.add("Disaster Phrases", None, *disaster_patterns)

            # convert the phrases into document object using nlp.make_doc to #speed up.
            phase_patterns = [nlp(text) for text in extended_phase_list]
            # add the patterns to the matcher object without any callbacks
            matcher.add("Phase Phrases", None, *phase_patterns)

            # convert the phrases into document object using nlp.make_doc to #speed up.
            problem_patterns = [nlp(text) for text in extended_problem_list]
            # add the patterns to the matcher object without any callbacks
            matcher.add("Problem Phrases", None, *problem_patterns)

            # convert the phrases into document object using nlp.make_doc to #speed up.
            method_patterns = [nlp(text) for text in extended_method_list]
            # add the patterns to the matcher object without any callbacks
            matcher.add("Method Phrases", None, *method_patterns)

            # convert the phrases into document object using nlp.make_doc to #speed up.
            simulation_outcome_patterns = [nlp(text) for text in extended_simulation_outcome_list]
            # add the patterns to the matcher object without any callbacks
            matcher.add("Simulation Outcome Phrases", None, *simulation_outcome_patterns)

            # convert the phrases into document object using nlp.make_doc to #speed up.
            simulation_method_patterns = [nlp(text) for text in simulation_method_list]
            # add the patterns to the matcher object without any callbacks
            matcher.add("Simulation Method Phrases", None, *simulation_method_patterns)

            # convert the phrases into document object using nlp.make_doc to #speed up.
            simulation_count_patterns = [nlp(text) for text in simulation_count_list]
            # add the patterns to the matcher object without any callbacks
            matcher.add("Simulation Count Phrases", None, *simulation_count_patterns)

            print("results for paper: " + paper)

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


if __name__ == "__main__":
    start = datetime.now()
    main()
    after = datetime.now()
    print("run startet at: " + start.strftime("%H:%M:%S"))
    print("run ended at: " + after.strftime("%H:%M:%S"))
    duration = after-start
    print("total runtime was: ")
    print(duration)