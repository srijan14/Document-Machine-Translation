# Import libraries
from PIL import Image
import pytesseract
import shutil
import os
from pdf2image import pdf2image
from translator import Translator
import requests
import json
import uuid
import re

class Convert:
    MODEL_PATH = os.path.abspath(os.path.join(os.getcwd(),"./model/model.pt"))
    def __init__(self,filename):
        self.filename = filename
        self.translator = Translator()
        self.translator.load_model(self.MODEL_PATH)
        self.image_out_path = os.path.join(os.getcwd(), "./data/images/")
        self.outfilename = os.path.join(os.path.dirname(self.filename),
                                                        "output",
                                        str(uuid.uuid1()) + "-hindi.txt")
        self.english = list()
        self.hindi = list()

    def extract_text(self):

        PDF_file = self.filename
        out_folder_name = os.path.basename(self.filename)

        if not os.path.exists(self.image_out_path):
            os.mkdir(self.image_out_path)

        if not os.path.exists(os.path.abspath(os.path.join(self.image_out_path,\
                out_folder_name))):
            os.mkdir(os.path.abspath(os.path.join(self.image_out_path,\
                out_folder_name)))


        index=0
        maxPages = pdf2image._page_count(PDF_file)
        for page in range(0, maxPages, 10):
            pages = pdf2image.convert_from_path(PDF_file, dpi=200,
                                              first_page=page,
                              last_page=min(page + 10 - 1, maxPages))
            for tpage in pages:
                tpage.save(os.path.abspath(os.path.join(self.image_out_path,
                                                       out_folder_name ,
                                                       str(index) + ".jpg"
                                                       )),'JPEG')
                index = index + 1


        print("Successfully saved images for each page for {}".format(self.image_out_path))

        english_text = list()

        for filename in sorted(os.listdir(os.path.join(self.image_out_path,
                                                        out_folder_name)),
                               key=lambda x:int(os.path.splitext(x)[0])):
            if filename.endswith("jpg"):
                text = str(((pytesseract.image_to_string(Image.open(os.path.join(self.image_out_path, out_folder_name,filename))))))
                text = text.replace('-\n', '')
                english_text.append(text)

        corpus = " ".join(english_text)
        corpus = re.sub(r'\n+', '\n', corpus).strip()
        corpus = corpus.split(".")
        self.english = list(map(str.strip, corpus))
        print("English Text Extracted is : {}".format(self.english))
        shutil.rmtree(self.image_out_path)


    def convert_text(self):

        for sourceText in self.english:
            output = self.translator.translate(sourceText,verbose=False)[0]
            self.hindi.append(output)

        print("Hindi Converted Text : {}".format(
            self.hindi))

    def create_pdf(self):

        f = open(self.outfilename, 'w')
        for item in self.hindi:
            f.write("%s\n" % item)
        f.close()

        return self.outfilename

if __name__=="__main__":
    c = Convert("/home/srijan/Desktop/self/github/English-Hindi/English-Hindi"
                "-Digital-Document-Translater/pdf_test_data/pdf1.pdf")
    c.extract_text()
    c.convert_text()