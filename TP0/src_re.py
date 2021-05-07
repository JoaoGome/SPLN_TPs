import requests
import re
import json
import urllib.request
from jjcli import *

from bs4 import BeautifulSoup



def run():
    print("Pressione: ")
    print("0: Receber um ficheiro JSON com a informação de todos os individuos.")
    print("1: Receber uma ontologia TURTLE com a informação de todos individuos.")
    print("2: Consultar a informação de um certo individuo.")
    print("3: Consultar a informação de um certo individuo num ficheiro.")
    print("9: Terminar.")
    resposta = input()

    while resposta != "9":
        if resposta == "0":
            with open('familia.json', 'w') as file:
                file.write(jsonO)
            print('\nInformação disponivel no ficheiro "familia.json"\n')
            
        elif resposta == "1":
            with open("ontologia_base.txt",'r') as ontFile:
                ontologiaBase = ontFile.read()
                with open("familia.ttl",'w') as ontTTL:
                    ontTTL.write(ontologiaBase)
                with open("familia.ttl",'a') as ontTTL:
                    ontTTL.write(ontologia)
            print('\nInformação disponivel no ficheiro "familia.ttl"\n')
            
        elif resposta == "2":
            print("\nIndique o ID do individuo.")
            resposta = input()
            for c in content:
                if c["Id"] == resposta:
                    print(json.dumps(c, sort_keys=False, indent=4, ensure_ascii=False))
                    break

        elif resposta == "3":
            print("\nIndique o ID do individuo.")
            resposta = input()
            for c in content:
                if c["Id"] == resposta:
                    with open("{nome}.json".format(nome=resposta),'w') as indFile:
                        indFile.write(json.dumps(c, sort_keys=False, indent=4, ensure_ascii=False))
                    break

        print("Pressione: ")
        print("0: Receber um ficheiro JSON com a informação de todos os individuos.")
        print("1: Receber uma ontologia TURTLE com a informação de todos individuos.")
        print("2: Consultar a informação de um certo individuo.")
        print("3: Consultar a informação de um certo individuo num ficheiro.")
        print("9: Terminar.")

        resposta = input()

#------------------------------------------ ////// ---------------------------

base_link = "http://pagfam.geneall.net/3418/"
individuos_ids = []
content = []  
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

    p = urllib.request.urlopen(base_link + individuo)
    pessoa = p.read().decode("utf8")

    id = individuo.split("=")[1]
    dataNascimento = ""
    dataMorte = ""
    localNascimento = ""
    localMorte = ""
    pai = ""
    idPai = ""
    mae = ""
    idMae = ""
    notas = []
    filhos = []
    idFilhos = []
    casamentos = []

    temPais = 0; temCasamentos = 0; temFilhos = 0
    if search(r'>Pais<', pessoa): temPais = 1
    if search(r'>Casamentos<', pessoa): temCasamentos = 1
    if search(r'>Filhos<', pessoa): temFilhos = 1

    # ---------------------------- Recolher info pessoa -----------------------------------
    if temPais:
        pessoa_info = search(r'<DIV align=center CLASS=head1>(\n|.)*</DIV>\n<div align="center">(\n|.)*</div>(.|\n)*(?=<div class="marcadorP" style="margin-top: 10px;">Pais</div>)', pessoa).group(0)
    elif temCasamentos:
        pessoa_info = search(r'<DIV align=center CLASS=head1>(\n|.)*</DIV>\n<div align="center">(\n|.)*</div>(.|\n)*(?=<div class="marcadorP" style="margin-top: 10px;">Casamentos</div>)', pessoa).group(0)
    else:
        print('Pessoa sem Casamentos nem Pais')

    nome = search(r'(?<=<DIV align=center CLASS=head1>)(\n|.)*(?=</DIV>)' , pessoa_info).group(0)

    infoNascimento = search(r'(?<=\*).*(?=div)' , pessoa_info)
    if infoNascimento:
        infoNascimento = infoNascimento.group(0)
        local_Nascimento = search(r'[^\<]*' , infoNascimento)
        data_Nascimento = search(r'(?<=<nobr>)[^\<]*' , infoNascimento)
        if local_Nascimento: localNascimento = local_Nascimento.group(0).strip()
        if data_Nascimento: dataNascimento = data_Nascimento.group(0).strip()

    infoMorte = search(r'(?<=\+).*(?=div)' , pessoa_info)
    if infoMorte:
        infoMorte = infoMorte.group(0)
        local_Morte = search(r'[^\<]*' , infoMorte)
        data_Morte = search(r'(?<=<nobr>)[^\<]*' , infoMorte)
        if local_Morte: localMorte = local_Morte.group(0).strip()
        if data_Morte: dataMorte = data_Morte.group(0).strip()


    # ---------------------------- Recolher info pais -----------------------------------

    if temPais:
        pessoa_pai = search(r'(?<=Pai:</B> <A)[^<]*', pessoa)
        if pessoa_pai:
            pessoa_pai_id = search(r'(?<=id=)[^>]*', pessoa_pai.group(0))
            pessoa_pai_nome = search(r'(?<=\>).*', pessoa_pai.group(0))
            if pessoa_pai_id: idPai = pessoa_pai_id.group(0)
            if pessoa_pai_nome: pai = pessoa_pai_nome.group(0).strip()

        pessoa_mae = search(r'(?<=Mãe:</B> <A)[^<]*', pessoa)
        if pessoa_mae:
            pessoa_mae_id = search(r'(?<=id=)[^>]*', pessoa_mae.group(0))
            pessoa_mae_nome = search(r'(?<=\>).*', pessoa_mae.group(0))
            if pessoa_mae_id: idMae = pessoa_mae_id.group(0)
            if pessoa_mae_nome: mae = pessoa_mae_nome.group(0).strip()



    # ---------------------------- Recolher info casamentos -----------------------------------
    
    if temCasamentos:
        pessoa_casamentos = search(r'(?<=Casamentos</div><div align="center")(\n|.)*(?=<div class="txt2">)', pessoa)
        
        mais_casamentos = search(r'(?<=Casamento)(\n|.)*', pessoa_casamentos.group(0))

        if not mais_casamentos:
            mais_casamentos = pessoa_casamentos

        while(mais_casamentos):
            cas = []

            info_Casamento = search(r'(?<=\>).*(?=<A)', mais_casamentos.group(0))

            local_Casamento = search(r'[^<]*', info_Casamento.group(0))
            data_Casamento = search(r'(?<=<nobr>)[^<]*', info_Casamento.group(0))


            conjuge_info = search(r'(?<=id=)[^<]*', mais_casamentos.group(0))
            conjuge_id = search(r'[^>]*', conjuge_info.group(0))
            conjuge_nome = search(r'(?<=>).*', conjuge_info.group(0))

            if local_Casamento: cas.append( local_Casamento.group(0).strip() )
            else: cas.append('')
            if data_Casamento: cas.append( data_Casamento.group(0).strip() )
            else: cas.append('')
            cas.append( conjuge_id.group(0).strip() )
            cas.append( conjuge_nome.group(0).strip() )

            casamentos.append(cas)

            mais_casamentos = search(r'(?<=Casamento)(\n|.)*', mais_casamentos.group(0))

    # ---------------------------- Recolher info filhos -----------------------------------
    
    if temFilhos:
        pessoa_filhos = search(r'(?<=Filhos</div>)(\n|.)*', pessoa)
        
        mais_filhos = search(r'(?<=Filhos)(\n|.)*', pessoa_filhos.group(0))

        if not mais_filhos:
            mais_filhos = pessoa_filhos

        while(mais_filhos):
            filhos_cas = sub(r'Filhos(.|\n)*', '', mais_filhos.group(0), count=1)

            nr_casamento = 0
            qual_casamento = search(r'I+', filhos_cas)
            if qual_casamento: nr_casamento = len(qual_casamento.group(0))

            cas_extra = search(r'(?<=(^ de <a)).*(?=<ul)', filhos_cas)
            if cas_extra: 
                cas_extra_conjuge_id = search(r'(?<=id=)[^">]*', cas_extra.group(0)).group(0)
                cas_extra_conjuge_nome = search(r'(?<=>)[^<]*', cas_extra.group(0)).group(0).strip()
                cas_extra_conjuge_data = search(r'(?<=nobr>).*(?=</nobr>)', cas_extra.group(0))
                if cas_extra_conjuge_data: cas_extra_conjuge_data = cas_extra_conjuge_data.group(0).strip()
                else: cas_extra_conjuge_data = ''

                casamentos.append(['',cas_extra_conjuge_data,cas_extra_conjuge_id,cas_extra_conjuge_nome])
                nr_casamento = len(casamentos)
                filhos_cas = sub(r'(?<=(^ de <a)).*(?=<ul)', '', filhos_cas, count=1)

            proximo_filho = search(r'(?<=id=)(\n|.)*', filhos_cas)
            

            filhos_casamento = []
            idFilhos_casamento = []
        
            while (proximo_filho):
                filho_info = search( r'[^<]*', proximo_filho.group(0) ).group(0).strip()
                filho_id = search( r'[^>"]*', filho_info ).group(0).strip()
                filho_nome = search( r'(?<=>).*', filho_info ).group(0).strip()

                filhos_casamento.append(filho_nome )
                idFilhos_casamento.append(filho_id )
                proximo_filho = search(r'(?<=id=)(\n|.)*', proximo_filho.group(0))
            
            while nr_casamento > len(filhos) + 1:
                filhos.append([])
                idFilhos.append([])
            filhos.append(filhos_casamento)
            idFilhos.append(idFilhos_casamento)

            mais_filhos = search(r'(?<=Filhos)(\n|.)*', mais_filhos.group(0))

        while len(casamentos) > len(filhos):
                filhos.append([])
                idFilhos.append([])

    nts = search(r'>Notas<(.|\n)*', pessoa)
    if nts:
        proxima_nota = search(r'(?<=<LI>)(.|\n)*', nts.group(0))

        while(proxima_nota):
            nota = search(r'[^<]*', proxima_nota.group(0)).group(0).strip()
            notas.append(nota)

            proxima_nota = search(r'(?<=<LI>)(.|\n)*', proxima_nota.group(0))


    #para guardar como json 

    info = {
        "Id": id,
        "Nome": "{name}".format(name=nome).strip(),
    }

    if dataNascimento != '': info['Data Nascimento'] = dataNascimento.strip()
    if localNascimento != '': info['Local Nascimento'] = localNascimento.strip()
    if dataMorte != '': info['Data Morte'] = dataMorte.strip()
    if localMorte != '': info['Local Morte'] = localMorte.strip()
    if pai != '': info['Pai'] = pai.strip()
    if mae != '': info['Mãe'] = mae.strip()
    if len(notas) > 0 : info['Notas'] = notas
    if len(casamentos) > 0:
        casamentosJSON = []
        for i, c in enumerate(casamentos):
            fi = []
            
            casamentoJSON = {
                "Conjuge": "{c}".format(c = c[3]).strip()
            }
            if c[0] != '': 
                casamentoJSON['Local'] = c[0].strip()
            if c[1] != '': 
                casamentoJSON['Data'] = c[1].strip()
            
            if len(filhos) > 0 and len(filhos[i]) > 0:
                casamentoJSON['Filhos'] = filhos[i]

            casamentosJSON.append(casamentoJSON)

        info["Casamentos"] = casamentosJSON
        
    content.append(info)

    # para guardar ontologia

    ont_casamentos = []

    ont_str = ':' + id + ' rdf:type owl:NamedIndividual , :Pessoa ;'
    ont_str += '\n:nome "' + nome.strip().replace(' ', '_') + '" ;'
    if (dataNascimento != ''): ont_str += '\n:dataNascimento "' + dataNascimento.strip() + '" ;'
    if (localNascimento != ''): ont_str += '\n:localNascimento "' + localNascimento.strip() + '" ;'
    if (dataMorte != ''): ont_str += '\n:dataMorte "' + dataMorte.strip() + '" ;'
    if (localMorte != ''): ont_str += '\n:localMorte "' + localMorte.strip() + '" ;'
    if (mae != ''): ont_str += '\n:mae :' + idMae.strip().replace(' ', '_') + ' ;'
    if (pai != ''): ont_str += '\n:pai :' + idPai.strip().replace(' ', '_') + ' ;'
    for n in notas:
        ont_str += '\n:notas "' + n.strip().replace('"', '') + '" ;'
    if (len(casamentos) > 0):
        for i, c in enumerate(casamentos):
            id_cas = ''.join(sorted(id + c[2]))
            ont_str += '\n:casamento :' + id_cas + ' ;'

            ont_cas = ':' + id_cas + ' rdf:type owl:NamedIndividual , :Casamento ;'
            ont_cas += '\n:conjuge :' + id + ' ;'
            ont_cas += '\n:conjuge :' + c[2] + ' ;'
            if(c[0] != ''): ont_cas += '\n:localCasamento "' + c[0].strip() + '" ;'
            if(c[1] != ''): ont_cas += '\n:dataCasamento "' + c[1].strip() + '" ;'
            if len(filhos):
                for f in idFilhos[i]:
                    if search(r'\"', f): print(f + ' ' + id)
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
