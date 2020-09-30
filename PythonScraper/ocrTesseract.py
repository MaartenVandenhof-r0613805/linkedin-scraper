from PIL import Image
import os
import pytesseract as pt
import os

pt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
directory = "./screenshots"

textFromScreenshots = []
for filename in os.listdir(directory):
    im = Image.open(directory + "/" + filename)
    #pt.image_to_pdf_or_hocr(im, lang="nl")
    text = pt.image_to_string(im, lang="nld")
    print(text)


