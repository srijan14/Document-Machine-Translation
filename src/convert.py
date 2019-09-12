# Import libraries
from PIL import Image
import pytesseract
import shutil
from pdf2jpg import pdf2jpg
import os
import urllib
import requests
import json
import time
import nltk
from fpdf import FPDF
import uuid
import re

class Convert:

    def __init__(self,filename):
        self.filename = filename
        self.image_out_path = os.path.join(os.getcwd(), "./data/images/")
        self.outfilename = os.path.join(os.path.dirname(self.filename),
                                                        "output",
                                        str(uuid.uuid1()) + "-hindi.txt")
        self.english = list()
        self.hindi = list()

    def extract_text(self):

        if not os.path.exists(self.image_out_path):
            os.mkdir(self.image_out_path)

        PDF_file = self.filename
        pdf2jpg.convert_pdf2jpg(PDF_file, self.image_out_path,dpi=300,
                                pages="0")
        print("Successfully saved images for each page for {}".format(self.image_out_path))

        out_folder_name = os.path.basename(self.filename) + "_dir"
        english_text = list()

        for filename in os.listdir(os.path.join(self.image_out_path,out_folder_name)):
            if filename.endswith("jpg"):
                text = str(((pytesseract.image_to_string(Image.open(os.path.join(self.image_out_path, out_folder_name,filename))))))
                text = text.replace('-\n', '')
                english_text.append(text)

        corpus = " ".join(english_text)
        corpus = re.sub(r'\n+', '\n', corpus).strip()
        self.english = corpus.split("\n")
        print("English Text Extracted is : {}".format(self.english))
        shutil.rmtree(self.image_out_path)


    def convert_text(self):

        for sourceText in self.english:
            resp = requests.post("http://localhost:5000/translator/translate",
                                 data=json.dumps([{"src": str(sourceText), "id": 100}])).json()
            output = resp[0][0]['tgt']
            self.hindi.append(output)
        print("Hindi Converted Text : {}".format(
            self.hindi))

    def create_pdf(self):

        f = open(self.outfilename, 'w')
        for item in self.hindi:
            f.write("%s\n" % item)
        f.close()

        return self.outfilename
