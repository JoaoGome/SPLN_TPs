import requests
import re
import json

from bs4 import BeautifulSoup

# função auxiliar para saber se uma string tem numeros no meio
def hasNumbers(string):
    for x in string:
        if x.isdigit():
            return True

    return False

# função que calcula o numero de ocorrencias de algo numa lista
def numberOf(element, list):
    result = 0
    for e in list:
        if element in e:
            result += 1
    
    return result

# função que calcula o numero de ocorrencias de algo enquanto que outro algo nao ocorreo numa lista 
def numberOf2(element1, element2, list):
    result = 0
    for e in list:
        if element1 in e and element2 not in e:
            result += 1
    
    return result

def run():
    print("Pressione: ")
    print("0: Receber a informação de todos os individuos num json.")
    print("1: Criar uma ontologia em turtle com a informação dos individuos.")
    print("2: Se desejar aceder a informação de um individuo em especifico.")
    print("3: Se desejar obter a informação de um individuo em ficheiro.")
    print("9: Se desejar terminar.")
    resposta = input()

    while resposta != "9":
        if resposta == "0":
            with open('info.json', 'w') as file:
                file.write(jsonO)
            print('Informação disponivel no ficheiro "info.json"')
            
        elif resposta == "1":
            with open("ontologia_base.txt",'r') as ontFile:
                ontologiaBase = ontFile.read()
                with open("ontologia.ttl",'w') as ontTTL:
                    ontTTL.write(ontologiaBase)
                with open("ontologia.ttl",'a') as ontTTL:
                    ontTTL.write(ontologia)
            print('Informação disponivel no ficheiro "info.ttl"')

        elif resposta == "2":
            print("Indique o ID do individuo.")
            resposta = input()
            for c in content:
                if c["Id"] == resposta:
                    print(json.dumps(c, sort_keys=False, indent=4, ensure_ascii=False))
                    break

        elif resposta == "3":
            print("Indique o ID do individuo.")
            resposta = input()
            for c in content:
                if c["Id"] == resposta:
                    with open("{nome}.json".format(nome=resposta),'w') as indFile:
                        indFile.write(json.dumps(c, sort_keys=False, indent=4, ensure_ascii=False))
                    break

        print("Pressione: ")
        print("0: Receber a informação de todos os individuos num json.")
        print("1: Criar uma ontologia em turtle com a informação dos individuos.")
        print("2: Se desejar aceder a informação de um individuo em especifico.")
        print("3: Se desejar obter a informação de um individuo em ficheiro.")
        print("9: Se desejar terminar.")

        resposta = input()

#------------------------------------------ ////// ---------------------------

base_link = "http://pagfam.geneall.net/3418/"
individuos_ids = []
content = []  # isto é suposto ser um array com a informação de cada individuo
ontologia = ""


# ------------- PARSE AOS HTMLS -------------

# ----- Conteudo da Pagina Inicial -----
firstPage = requests.get(base_link)
firstSoup = BeautifulSoup(firstPage.text, "html.parser")

# Ir buscar o link para a página com todos os links por pessoa e por familia
for firstLink in firstSoup.find_all('a'):
    if ((firstLink.get_text() == "Ver todas") and ("pessoas" in firstLink.get('href'))):
        pessoas_link = firstLink.get('href')

    elif ((firstLink.get_text() == "Ver todas") and ("familias" in firstLink.get('href'))):
        familias_link = firstLink.get('href')

# ----- Conteudo da Pagina das Pessoas -----
pessoasPage = requests.get(base_link + pessoas_link)
pessoasSoup = BeautifulSoup(pessoasPage.text, "html.parser")

for pessoasLink in pessoasSoup.find_all('a'):
    ref = str(pessoasLink.get('href'))
    match = re.search(r'id=([0-9]+)', ref)

    # estamos nos links dos individuos
    if(match):
        individuos_ids.append(ref)

    # estamos nos links que dao para as outras paginas com o resto dos individuos
    else:
        match = re.search(r'idx', ref)
        if(match):
            pessoaPage = requests.get("http://pagfam.geneall.net" + match.string)
            pessoaSoup = BeautifulSoup(pessoaPage.text, "html.parser")

            for pessoaLink in pessoaSoup.find_all('a'):
                ref = str(pessoaLink.get('href'))
                match = re.search(r'id=([0-9]+)', ref)
                if(match):
                    individuos_ids.append(ref)


# ----- Percorrer os ids todos e ir buscar a info de cada pagina -----

for individuo in individuos_ids:
    indPage = requests.get(base_link + individuo)
    indSoup = BeautifulSoup(indPage.text, "html.parser")
    string_aux = []

    # buscar o nome que está na tag title
    nome = indSoup.find('title').get_text()

    id = individuo.split("=")[1]
    dataNascimento = ""
    dataMorte = ""
    localNascimento = ""
    localMorte = ""
    pai = ""
    mae = ""
    notas = []
    filhos = []
    casamentos = []

    # ir buscar as notas
    ulTags = indSoup.find_all('ul')
    for ul in ulTags:
        if(ul.has_attr('class')):
            if(str(ul['class'][0]) == "txt2"):
                liSoup = BeautifulSoup(str(ul),"html.parser")
                liTags = liSoup.find_all('li')
                for li in liTags:
                    notas.append(li.get_text().strip())

    # ir buscar os Filhos

    if("Filhos" in indSoup.strings):

        numeroFilhos = numberOf("Filhos",indSoup.strings)
        check = 0
        divTags = indSoup.find_all('div')

        for div in divTags:
            if(div.has_attr('class')):
                
                if(str(div['class'][0]) == "txt2"):
                    listaSoup = BeautifulSoup(str(div),"html.parser")
                    ulTags = listaSoup.find_all('ul')
                    for ul in ulTags:
                        
                        if (check < (numeroFilhos - 1) or ((numeroFilhos == 1) and not check)) :
                            filhosCasamento = []
                            check += 1
                            liSoup = BeautifulSoup(str(ul),"html.parser")
                            liTags = liSoup.find_all('li')
                            for li in liTags:
                                aSoup = BeautifulSoup(str(li),"html.parser")
                                aTags = aSoup.find_all('a')
                                for a in aTags:
                                    filhosCasamento.append(a.get_text().strip())

                            if numeroFilhos == 2 and ("Filhos do Casamento II:" in indSoup.strings):
                                filhos.append([])
                            filhos.append(filhosCasamento)
                            if numeroFilhos == 2 and ("Filhos do Casamento I:" in indSoup.strings):
                                filhos.append([])
                        
                    
    # ir buscar os casamentos
    if ("Casamentos" in indSoup.strings):

        numeroCasamentos = numberOf2("Casamento","Filho",indSoup.strings)
        check = 0
        anotherCheck = 0
        divTags = indSoup.find_all('div')
        for div in divTags:
            if(div.has_attr('class')):
                if(str(div['class'][0]) == "txt2"):
                    listaSoup = BeautifulSoup(str(div),"html.parser")
                    div2Tags = listaSoup.find_all('div')
                    for div2 in div2Tags:
                        
                        if(div2.has_attr('class') and str(div2['class'][0]) == "marcadorP" and div2.get_text()=="Casamentos"):
                            anotherCheck = 1
                        
                        aSoup = BeautifulSoup(str(div2),"html.parser")
                        aTags = aSoup.find_all('a')

                        cas = []
                        if (anotherCheck == 1 and numeroCasamentos > 0):
                            if(div2.has_attr('align') and str(div2['align']) == "center" and not div2.has_attr('style')):
                                for x in div2.stripped_strings:
                                    if x != "Casamento I:" and x != "Casamento II:":
                                        if re.search(r'[0-9.]+', x):
                                            if(len(cas) == 0):
                                                cas.append('')
                                            cas.append(x)
                                        else:
                                            cas.append(x)
                                if len(cas) == 0:
                                    cas.append('')
                                if len(cas) == 1:
                                    cas.append('')
                                casamentos.append(cas)
                                cas = []
                            if( (check < (numeroCasamentos - 1) or check == 0)):
                                for a in aTags:
                                    if(check == 0 or check < (numeroCasamentos - 1)):
                                        casamentos[check].append(a.get_text().strip())
                                        check += 1
                                    
            
        if (not len(casamentos)):
            found = 0
            check = 0
            for div in divTags:
                
                if (not found):
                    aux = []
                    for x in div.stripped_strings:
                        aux.append(x)
                    if (len(aux) == 1 and x == "Casamentos"):
                        found = 1
                        aux = []
                elif(numeroCasamentos > 0 and (check == 0 or check < (numeroCasamentos - 1))):
                    aSoup = BeautifulSoup(str(div),"html.parser")
                    aTags = aSoup.find_all('a')
                    stop = 0
                    for x in div.stripped_strings:
                        if x != "Casamentos" and not stop:
                            if x == '*':
                                stop = 1
                            else:
                                aux.append(x)
                    
                    for a in aTags:
                        if (check == 0 or check < (numeroCasamentos - 1)):
                            #casamentos.append(a.get_text().strip())
                            check += 1
                            if len(aux) == 3:
                                casamentos.append(aux)
                            if len(aux) == 2:
                                if re.search(r'[0-9.]+', aux[0]):
                                    casamentos.append(['',aux[0],aux[1]])
                                else:
                                    casamentos.append([aux[0],'',aux[1]])
                            if len(aux) == 1:
                                casamentos.append(['','',aux[0]])

    # ir buscar birth, death, pais
    for x in indSoup.stripped_strings:
        string_aux.append(x)

    for i in range(len(string_aux)):
        if ("*" in string_aux[i] and len(string_aux[i]) > 1):
            if (hasNumbers(string_aux[i])):
                dataNascimento = string_aux[i].strip("*")
            
            else:
                localNascimento = string_aux[i].strip("*")
                if (hasNumbers(string_aux[i+1])):
                    dataNascimento = string_aux[i+1]

        if ("+" in string_aux[i] and len(string_aux[i]) > 1):
            if (hasNumbers(string_aux[i])):
                dataMorte = string_aux[i].strip("+")
            
            else:
                localMorte = string_aux[i].strip("+")
                if (hasNumbers(string_aux[i+1])):
                    dataMorte = string_aux[i+1]

        if ("Pai:" in string_aux[i]):
            pai = string_aux[i+1]

        if("Mãe:" in string_aux[i]):
            mae = string_aux[i+1]

    #para guardar como json 

    info = {
        "Id": id,
        "Nome": "{name}".format(name=nome).strip(),
        "Data Nasc": "{data}".format(data = dataNascimento).strip(),
        "Local Nasc": "{local}".format(local = localNascimento).strip(),
        "Data Morte": "{data}".format(data = dataMorte).strip(),
        "Local Morte": "{local}".format(local = localMorte).strip(),
        "Pai": "{pai}".format(pai = pai).strip(),
        "Mãe": "{mae}".format(mae = mae).strip(),
        "Notas": notas
    }

    casamentosJSON = []

    for i, c in enumerate(casamentos):
        fi = []
        if len(filhos):
            fi = filhos[i]
        casamentoJSON = {
            "Conjuge": "{c}".format(c = c[2]).strip(),
            "Local": "{l}".format(l = c[0]).strip(),
            "Data": "{d}".format(d = c[1]).strip(),
            "Filhos": fi
        }
        casamentosJSON.append(casamentoJSON)

    info["Casamentos"] = casamentosJSON
        
    content.append(info)

    ont_casamentos = []

    ont_str = ':' + nome.strip().replace(' ', '_') + ' rdf:type owl:NamedIndividual , :Pessoa ;'
    ont_str += '\n:nome "' + nome.strip().replace(' ', '_') + '" ;'
    if (dataNascimento != ''): ont_str += '\n:dataNascimento "' + dataNascimento.strip() + '" ;'
    if (localNascimento != ''): ont_str += '\n:localNascimento "' + localNascimento.strip() + '" ;'
    if (dataMorte != ''): ont_str += '\n:dataMorte "' + dataMorte.strip() + '" ;'
    if (localMorte != ''): ont_str += '\n:localMorte "' + localMorte.strip() + '" ;'
    if (mae != ''): ont_str += '\n:mae :' + mae.strip().replace(' ', '_') + ' ;'
    if (pai != ''): ont_str += '\n:pai :' + pai.strip().replace(' ', '_') + ' ;'
    if (len(notas) > 0): ont_str += '\n:notas "' + ' ; '.join(notas).strip().replace('"', '') + '" ;'
    if (len(casamentos) > 0):
        for i, c in enumerate(casamentos):
            regex = re.compile('[^A-Z]')
            id1 = regex.sub('', c[2].strip() + nome.strip())
            regex = re.compile('[^0-9]')
            id2 = regex.sub('', c[1].strip())
            id_cas = ''.join(sorted(id1)) + id2
            ont_str += '\n:casamento :' + id_cas + ' ;'

            ont_cas = ':' + id_cas + ' rdf:type owl:NamedIndividual , :Casamento ;'
            ont_cas += '\n:conjuge :' + nome.strip().replace(' ', '_') + ' ;'
            ont_cas += '\n:conjuge :' + c[2].strip().replace(' ', '_') + ' ;'
            if(c[0] != ''): ont_cas += '\n:localCasamento "' + c[0].strip() + '" ;'
            if(c[1] != ''): ont_cas += '\n:dataCasamento "' + c[1].strip() + '" ;'
            if len(filhos):
                for f in filhos[i]:
                    ont_cas += '\n:filho :' + f.strip().replace(' ', '_') + " ;"
                    ont_str += '\n:filho :' + f.strip().replace(' ', '_') + " ;"
            ont_cas += ' .'

            ont_casamentos.append(ont_cas)
    ont_str += ' .'
    ontologia += '\n\n' + ont_str
    for s in ont_casamentos:
        ontologia += '\n\n' + s

jsonO = json.dumps(content, indent=4, ensure_ascii=False)

run()
