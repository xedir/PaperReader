import PyPDF2
import spacy
from spacy.matcher import Matcher
from spacy.language import Language
import os
from tika import parser


# method for reading a pdf file
def readPdfFile_tika(path, filename):
    # storing path of PDF-Documents folder
    file = open(path + "/" + filename, mode="rb")

    parsed = parser.from_file(path+ "/" +filename)

    full_text = parsed["content"]

    return full_text

# customer sentence segmenter for creating spacy document object
@Language.component("setCustomBoundaries")
def setCustomBoundaries(doc):
    # traversing through tokens in document object
    for token in doc[:-1]:
        if token.text == ';':
            doc[token.i + 1].is_sent_start = True
        if token.text == ".":
            doc[token.i + 1].is_sent_start = False
    return doc

# create spacy document object from pdf text
def getSpacyDocument(pdf_text, nlp):
    main_doc = nlp(pdf_text)  # create spacy document object

    return main_doc



# method for reading a pdf file
def readPdfFile(path, filename):
    # storing path of PDF-Documents folder
    file = open(path + "/" + filename, mode="rb")

    # looping through pdf pages and storing data
    pdf_reader = PyPDF2.PdfFileReader(file, "rb")
    num_pages = pdf_reader.numPages

    # traverse through each page and store data as an element in list
    text = []
    for pages in range(0, num_pages):
        current_page = pdf_reader.getPage(pages)
        text.append(current_page.extractText().replace("\n", "").lower())

    # # remove \n from list
    # text = [t.replace("\n", "").lower() for t in text]

    # store content of 1-last page in a seperate list
    rest_pages = []
    for t in text[1:]:
        rest_pages.append(t[115:])

    # store 0th page content separately
    first_page = [text[0][850:]]

    # storing the 0th and 1-last page content after cleaning in text
    text = first_page + rest_pages

    # creating a single string containing full text
    full_text = "".join(text)

    return full_text



def processPDF(path, name):

    # spacy english model (large)
    pdf_text = readPdfFile_tika(path, name)

    return pdf_text
    #setCustomBoundaries(doc)

