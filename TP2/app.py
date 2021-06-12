import xmlParser
import sys
import os
import json

from flask import Flask, render_template, request, redirect
UPLOAD_FOLDER = './files/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# exemplo: python3 app.py inputTemplate.xml -csv ou python3 app.py inputTemplate.xml -json
if (len(sys.argv) < 3):
    print("Não passou ficheiro xml de config ou formato do ficheiro de resposta")
    exit()

info = xmlParser.parseFile(sys.argv[1])
results = sys.argv[2][1:]
print(info)
id = info["id"]
info.pop("id")

html = f'''
        <html>
            <body>
                <p>{id}</p>
                <form action = "http://localhost:8000/upload" method = "POST" enctype = "multipart/form-data">
        '''

for (key,value) in info.items():
    if (value["type"] == "select"): 
        html += f'''
                    <p>{value["title"]} </p>
                '''

        for (key2,value2) in value.items():
            if (key2 != "type" and key2 != "title") :
                html += f'''
                            <input type="radio" id="{value2}" name="{value["title"]}" value="{value2}">
                            <label for="{value["title"]}">{value2}</label>
                        '''

    else:
        html += f'''
                <p>{value["text"]} </p>
                <div class="form-group">
                    <input type="{value["type"]}" class="form-control" id="{value["text"]}" name="{value["text"]}"
                </div>
                ''' 

html += f'''
        <input type = "submit" />
        </form>
        </body>
        </html>
        '''

@app.route('/')
def base():
    return html 

@app.route('/upload', methods = ['POST'])
def upload():
    
    dic = {}
    first = True
    for x in info.values():
        if x["type"] == "file":
            f = request.files[x["text"]]
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            dic[x["text"]] = f.filename
    
        elif x["type"] == "select":
            dic[x["title"]] = request.form[x["title"]] 

        else:
            dic[x["text"]] = request.form[x["text"]]

    if (results == "csv"):
        if (not os.path.isfile('./results.csv')):
            with open('results.csv','w') as f:
                headers = ""
                for x in dic.keys():
                    headers += f'''{x},'''
                f.write(headers[:-1]+'\n')

        with open('results.csv','a') as f:
            for x in dic.values():
                if first:
                    f.write(f'''{x}''')
                    first = False 
                else:
                    f.write(',')
                    f.write(f'''{x}''')
            
            f.write('\n')

    elif (results == "json"):
        data = []
        if (not os.path.isfile('./results.json')):
            with open('results.json','w') as f:
                f.write('[]')
        
        with open('results.json','r') as f:
            data = json.load(f)

        data.append(dic)

        with open('results.json','w') as f:
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


