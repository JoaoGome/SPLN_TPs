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

#------------------------------------------ ////// ---------------------------

base_link = "http://pagfam.geneall.net/3418/"
#individuoBase_link = "http://pagfam.geneall.net/3418/pessoas.php?id=" #link base para pagina de um dado individuo
individuos_ids = []
content = []  # isto é suposto ser um array com a informação de cada individuo


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
        #print('--------------------------------------')

        numeroCasamentos = numberOf2("Casamento","Filho",indSoup.strings)
        check = 0
        anotherCheck = 0
        divTags = indSoup.find_all('div')
        for div in divTags:
            if(div.has_attr('class')):
                if(str(div['class'][0]) == "txt2"):
                    listaSoup = BeautifulSoup(str(div),"html.parser")
                    div2Tags = listaSoup.find_all('div')
                    aux = []
                    for div2 in div2Tags:
                        aux = []
                        if(div2.has_attr('class') and str(div2['class'][0]) == "marcadorP"):
                            anotherCheck = 1

                        aSoup = BeautifulSoup(str(div2),"html.parser")
                        aTags = aSoup.find_all('a')
                        if (anotherCheck == 1 and numeroCasamentos > 0):
                            if( (check < (numeroCasamentos - 1) or check == 0)):
                                stop = -1
                                #print("!!!!!!!!!!!!!!!!!_______________________-")
                                cas = []
                                for x in div.stripped_strings: 
                                    print(stop)
                                    if (x == "Casamentos"):
                                        stop = 0
                                        aux = []
                                        #print("--casamentos")
                                    elif stop == 0:
                                        if (x == "Casamento I"):
                                            #print("--casamento 1")
                                            stop = 1
                                        else:
                                            cas.append(x)
                                    elif stop == 1:
                                        if (x == "Casamento II"):
                                            if len(cas) == 3:
                                                casamentos.append(cas)
                                            if len(cas) == 2:
                                                if re.search(r'[0-9.]+', cas[0]):
                                                    casamentos.append(['',cas[0],cas[1]])
                                                else:
                                                    casamentos.append([cas[0],'',cas[1]])
                                            if len(cas) == 1:
                                                casamentos.append(['','',cas[0]])
                                            #print(cas)
                                            
                                            #print("--casamento 2")
                                            
                                            #casamentos.append(cas)
                                            cas = []
                                        elif(x == '*'):
                                            stop = 0
                                        else:
                                            cas.append(x)

                                if len(cas) == 3:
                                    casamentos.append(cas)
                                if len(cas) == 2:
                                    if re.search(r'[0-9.]+', cas[0]):
                                        casamentos.append(['',cas[0],cas[1]])
                                    else:
                                        casamentos.append([cas[0],'',cas[1]])
                                if len(cas) == 1:
                                    casamentos.append(['','',cas[0]])
                                print(cas)
                                
                                #casamentos.append(cas)
                                cas = []
                                #print(casamentos)
                                #casamentos.append(cas)

                                '''for a in aTags:
                                    if(check == 0 or check < (numeroCasamentos - 1)):
                                        casamentos.append(a.get_text().strip())
                                        print(aux)
                                        #print(a.get_text())
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
                                    aux = []
                                aux = []'''
            
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
    
    
    #print(casamentos)

    info = {
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
    #if len(filhos):
        #print(filhos)
    for i, c in enumerate(casamentos):
        fi = []
        if len(filhos):
            fi = filhos[0]
        casamentoJSON = {
            "Conjuge": "{c}".format(c = c).strip(),
            "Local": "",
            "Data": "",
            "Filhos": fi
        }
        casamentosJSON.append(casamentoJSON)

    info["Casamentos"] = casamentosJSON
        

    content.append(info)

jsonO = json.dumps(content, indent=4, ensure_ascii=False)
#print(jsonO)

