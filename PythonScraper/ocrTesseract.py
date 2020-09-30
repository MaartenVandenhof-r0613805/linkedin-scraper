from PIL import Image
from fpdf import FPDF
import pytesseract as pt
import os

pt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
directory = "./screenshots"

pdfFiles = []
titleInt = 1
for filename in os.listdir(directory):
    im = Image.open(directory + "/" + filename)
    pdf = pt.image_to_pdf_or_hocr(im, lang="nld", extension="pdf")
    
    # Write to PDF
    with open("./pdfFiles/pdf_" + str(titleInt) + ".pdf", "w+b") as f:
        f.write(pdf)
    f.close()
    print("file " + str(titleInt) + " written")
    titleInt = titleInt + 1

    #text = pt.image_to_string(im, lang="nld")