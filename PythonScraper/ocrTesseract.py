from PIL import Image
import pytesseract as pt
import os
import glob

# Works only on Windows
pt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Set screenshot directory
directory = "./screenshots"

# Remove old contents pdf folder
files = glob.glob('./pdfFiles/*')
for f in files:
    os.remove(f)

# Screenshot to text and PDF
pdfFiles = []
titleInt = 1
for filename in os.listdir(directory):
    # Convert image to text/PDF
    im = Image.open(directory + "/" + filename)
    pdf = pt.image_to_pdf_or_hocr(im, lang="nld", extension="pdf")

    # Write to PDF
    with open("./pdfFiles/pdf_" + str(titleInt) + ".pdf", "w+b") as f:
        f.write(pdf)
    f.close()
    print("file " + str(titleInt) + " written")
    titleInt = titleInt + 1
