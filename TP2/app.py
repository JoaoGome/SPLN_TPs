import xmlParser
import sys

from flask import Flask, render_template, request
app = Flask(__name__)

if (len(sys.argv) < 2):
    print("Não passou ficheiro xml de config!")
    exit()

info = xmlParser.parseFile(sys.argv[1])

'''
@app.route('/')
def form():
   '''

info.pop("id")

for x,y in info.items():
    print("Type ", y["type"])
    print("Text ", y["text"])
