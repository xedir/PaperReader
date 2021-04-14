import spacy
import numpy as np
from sense2vec import Sense2VecComponent


def most_similar_single(word):
    nlp = spacy.load('en_core_web_lg')
    s2v = nlp.add_pipe("sense2vec")
    s2v.from_disk("/Users/Nic/PycharmProjects/PaperReader/s2v_reddit_2019_lg")

    doc = nlp(word)
    l = doc.__len__()+1

    #print(doc.vocab[0])
    assert doc[0:l].text == word
    freq = doc[0:l]._.s2v_freq
    vector = doc[0:l]._.s2v_vec
    most_similar_words = doc[0:l]._.s2v_most_similar(5)

    #print("Similar words to keyword: " + word)
    print(most_similar_words)

    return most_similar_words

#most_similar('supply chain')


def most_similar_list(liste):
    nlp = spacy.load('en_core_web_lg')
    s2v = nlp.add_pipe("sense2vec")
    s2v.from_disk("/Users/Nic/PycharmProjects/PaperReader/s2v_reddit_2019_lg")

    results = liste
    temp = []

    for element in liste:
        doc = nlp(element)
        l = doc.__len__()+1

        #print(doc.vocab[0])
        assert doc[0:l].text == element
        freq = doc[0:l]._.s2v_freq
        vector = doc[0:l]._.s2v_vec
        most_similar_words = doc[0:l]._.s2v_most_similar(3)

        for elem in most_similar_words:
            temp.append(elem[0][0])
            print(elem[0][0])
    results = liste + temp
    print(results)
    return results


# to run this script and get similar keywords insert a "seed" keyword list as shown below and run most_similar_list(liste)
# extended_problem_list = ['evacuation','procurement','allocate','allocation','coordinate','coordination','evacuate','manufacture','market allocation','material handling','personal transport','personal transportation','procure','procurement process','resource allocation','resource distribution','risk analysis','risk assessment','risk management','risk','training','transport','transportation',
#  'warehouse work','warehousing', 'capacity','staff', 'information collection','information sharing']
# most_similar_list(extended_problem_list)

# list = ['dog', 'cat', 'car']
# most_similar_list(list)