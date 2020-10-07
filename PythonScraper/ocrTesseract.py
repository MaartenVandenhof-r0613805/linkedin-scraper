from PIL import Image
import pytesseract as pt
import os
import glob
import json

# Works only on Windows
pt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# FUNCTIONS
# Add text from image to jsonElement
def addTextToJson(jsonElement, textJsonName, imagePath):
    im = Image.open(str(imagePath))
    content = pt.image_to_string(im, lang="nld")
    jsonElement[str(textJsonName)] = content
    print("json text added from " + imagePath)


# SCRIPT
# Remove old contents pdf folder
files = glob.glob('./pdfFiles/*')
for f in files:
    os.remove(f)

# Load Json data
data = {}
with open('./data/WebscrapeData.json') as json_file:
    data = json.load(json_file)
    json_file.close()

# Add to Json
for line in data:
    for element in data[str(line)]:
        addTextToJson(element, 'content', element['screenshotPath'])

# Write to Json file
with open('./data/WebscrapeData.json', 'w') as out:
    json.dump(data, out)
