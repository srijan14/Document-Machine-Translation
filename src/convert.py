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
        print(self.outfilename)
        self.english = list()
        self.hindi_own = list()
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
        # self.english = nltk.sent_tokenize(corpus)
        self.english = corpus.split("\n")
        print("English Text Extracted is : {}".format(self.english))
        shutil.rmtree(self.image_out_path)

    def convert_text(self):
        sourceLang = "en"
        targetLang = "hi"
        for sourceText in self.english:
            time.sleep(4)
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl="+ sourceLang + "&tl=" + targetLang + "&dt=t&q=" + urllib.parse.quote(str(sourceText))
            resp = requests.get(url)
            output = json.loads(resp.text)[0][0][0].strip()
            self.hindi.append(output)
        print("Hindi Converted Text by google api is : {}".format(self.hindi))


    def convert_text_own(self):

        for sourceText in self.english:
            resp = requests.post("http://localhost:5000/translator/translate",data=json.dumps([{"src": str(sourceText), "id": 100}])).json()
            output = resp[0][0]['tgt']
            self.hindi_own.append(output)
        print("Hindi Converted Text by own model is : {}".format(
            self.hindi_own))

    def create_pdf(self):

        pdf = FPDF()
        pdf.add_page()

        # pdf.add_font('gargi', '', 'gargi.ttf', uni=True)
        # pdf.set_font('gargi', '', 14)
        # pdf.write(8, u'Hindi: नमस्ते दुनिया')

        # pdf.set_font("Arial", size=12,uni=True)
        # pdf.cell(200, 10, txt=u" ".join(self.hindi), ln=1, align="C")
        # pdf.output(self.outfilename)
        f = open(self.outfilename, 'w')
        for item in self.hindi:
            f.write("%s\n" % item)
        f.close()

        return self.outfilename


    def create_pdf_own(self):

        f = open(self.outfilename, 'w')
        for item in self.hindi_own:
            f.write("%s\n" % item)
        f.close()

        return self.outfilename


if __name__=="__main__":
    con = Convert(os.path.join(os.getcwd(),"./pdf_test_data/send.pdf"))

    print("Starting Data Extraction Module")
    con.extract_text()
    # con.english = ['| am an Analytics and Machine learning professional, B.Tech IIT Delhi and MBA IIM Udaipur, with\nvast experience across different aspects of data science and engineering.', '| am looking for a\nchallenging job which enables me to build or transform the analytics/ data science team for a\ncompany, preferably with a team.', '| am also willing to work in companies that belong to core industries\nand are looking to utilize data to transform their processes through advanced analytics.', '| attained significant interest in the area of math, stats and probability during my JEE preparation\nitself.', '| received preliminary formal education in the field through the courses studied at IIT Delhi and\nco-curricular participations.', 'In addition to learning the quantitative and practical aspects of civil\nengineering; | also pursued statistical courses like Probability and statistics, financial mathematics\nand Econometric methods along with a minor in business management.', '| joined UHG after my\nundergraduate and worked extensively on deriving intelligence out of data through engineering and\nscience pertaining to prospective care opportunities.', 'Given my experience with the data and business\nintelligence, | decided to pursue all the available Analytics/ML courses at IIM Udaipur which include\nStatistics, Predictive Analytics | and Il, Operations research, Marketing Analytics and Financial Time\nSeries in R. | also pursued a 5 course Deep learning Specialization certification, includes lectures and\npython programming assignments, taught by Andrew NG on Coursera.', '| joined ICICI!', 'Lombard as business analyst and decided to join the data science team.', 'There, |\nworked on developing ML oriented to business problems like cross selling, fraud detection and Claims\namount prediction.', 'Currently | am working with PwC DIAC on a sales forecasting model for a client.', '|\nhave also worked on modelling inventory optimisation and customer renewal rate/churn analysis.', 'Given my experience in data warehouse aspects (extraction, storage, manipulation, automation);\nData science Techniques (Segmentation, Classification, Forecasting and Regression and deep\nlearning techniques) and Business analytics aspects (Deep understanding of business processes,\ndata visualization, presentation) make me a perfect fit for multi-dimensional job enabling me to deliver\nvalue to my potential.']

    # print("Starting Data Conversion Module")
    # con.convert_text_own()

    # print(con.create_pdf_own())
