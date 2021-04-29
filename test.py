#%%
from PyPDF2 import PdfFileReader
import os

#%%
path = r"C:\Users\henke\Documents\PRpapers"
os.chdir(path)
for f in os.listdir():
    r = f.replace(" ","_")
    if( r != f):
        os.rename(f,r)

#%%
def get_info(filepath):
    with open(filepath, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    
    return info.title

if __name__ == '__main__':
    path = r"C:\Users\henke\Documents\PRpapers"
    arr = os.listdir(path)

    for file in arr:
        filepath = path + "/" + file
        a = get_info(filepath)
        if (a != None) and (a != ""):
            newfile = path  + "/" + a + ".pdf"
            os.rename(filepath, newfile)
            print("I did it")
