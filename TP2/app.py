import xmlParser
import sys
import os
import json

from flask import Flask, render_template, request, redirect

UPLOAD_FOLDER = './files/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# exemplo: python3 app.py inputTemplate.xml -csv ou python3 app.py inputTemplate.xml results.json
if (len(sys.argv) < 3):
    print("Não passou ficheiro xml de config ou nome do ficheiro de resposta")
    print("Exemplo: python3 app.py inputTemplate.xml results.json")
    exit()

info = xmlParser.parseFile(sys.argv[1])
results = sys.argv[2]
print(info)

html = xmlParser.createHTML(info)

@app.route('/')
def base():
    return html 

@app.route('/upload', methods = ['POST'])
def upload():
    dic = {}
    first = True

    for x in info.values():

        if x["type"] == "file":
            if request.files[x["text"]]:
                f = request.files[x["text"]]
                i = 0
                newname = f.filename
                while os.path.isfile(f'{app.config["UPLOAD_FOLDER"]}/{newname}'):
                    newname = f'({i}).'.join(f.filename.split('.'))
                    i += 1
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], newname))
                dic[x["text"]] = newname
    
        elif x["type"] == "select":
            if x["title"] in request.form:
                dic[x["title"]] = request.form[x["title"]] 

        elif x["text"] in request.form:
            dic[x["text"]] = request.form[x["text"]]

    if (results.split('.')[1] == "csv"):
        if (not os.path.isfile(f'./{results}')):
            with open(f'./{results}','w') as f:
                headers = ""
                for x in dic.keys():
                    headers += f'''{x},'''
                f.write(headers[:-1]+'\n')

        with open(f'./{results}','a') as f:
            for x in dic.values():
                if first:
                    f.write(f'''{x}''')
                    first = False 
                else:
                    f.write(',')
                    f.write(f'''{x}''')
            
            f.write('\n')

    elif (results.split('.')[1] == "json"):
        data = []
        if (not os.path.isfile(f'./{results}')):
            with open(f'./{results}','w') as f:
                f.write('[]')
        
        with open(f'./{results}','r') as f:
            data = json.load(f)

        data.append(dic)

        with open(f'./{results}','w') as f:
            f.write(json.dumps(data,indent=4))

    return redirect("/")

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8000)




# exemplo da estrutura do dicionario que resulta de dar parse ao xml
{
    'id': 'Formulário Teste', 
    
    'item1': 
    {
        'type': 'number', 
        'text': 'Idade'
    }, 
    'item2': 
    {
        'type': 'text', 
        'text': 'Nome'
    }, 
    'item3': 
    {
        'type': 'select', 
        'title': 'Sex', 
        'text1': 'Boy', 
        'text2': 'Girl', 
        'text3': 'Other'
    }, 
    'item4': 
    {
        'type': 'file', 
        'text': 'Fotografia'
    }
}


