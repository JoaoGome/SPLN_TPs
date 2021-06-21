import xml.etree.ElementTree as ET

def parseFile (filePath:str):

    dict = {}
    itemID = 1
    tree = ET.parse(filePath)

    rootElement = tree.getroot()

    for child in rootElement:
        if (child.tag == "title"):
            dict["title"] = f"{child.text}"

        elif (child.tag == "item"):
            tempDict = {}
            textID = 1
            if (child.attrib["type"] == "radio"):
                tempDict["type"] = "radio"
                for itemChild in child:
                    if (itemChild.tag == "title"):
                        tempDict["title"] = f"{itemChild.text}"
                    elif (itemChild.tag == "text"):
                        tempDict[f"text{textID}"] = f"{itemChild.text}"
                        textID += 1
                dict[f"item{itemID}"] = tempDict
                itemID += 1

            elif (child.attrib["type"] == "checkbox"):
                tempDict["type"] = child.attrib["type"]
                tempDict["text"] = []
                for itemChild in child:
                    if (itemChild.tag == "title"):
                        tempDict["title"] = f"{itemChild.text}"
                    elif (itemChild.tag == "text"):
                        tempDict[f"text"].append(f"{itemChild.text}")
                dict[f"item{itemID}"] = tempDict
                itemID += 1

            elif (child.attrib["type"] == "select"):
                tempDict["type"] = child.attrib["type"]
                tempDict["text"] = []
                for itemChild in child:
                    if (itemChild.tag == "title"):
                        tempDict["title"] = f"{itemChild.text}"
                    elif (itemChild.tag == "text"):
                        tempDict[f"text"].append(f"{itemChild.text}")
                dict[f"item{itemID}"] = tempDict
                itemID += 1

            else:
                tempDict["type"] = child.attrib["type"]
                for itemChild in child:
                    if (itemChild.tag == "text"):
                        tempDict["text"] = f"{itemChild.text}"
            
                dict[f"item{itemID}"] = tempDict
                itemID += 1

    return dict


def createHTML(info: dict):
    title = info["title"]
    info.pop("title")

    html = f'''
        <html>
            <head>
                <title>{title}</title>
                <meta charset="utf-8"/>
                <link rel="stylesheet" href="C:/Users/Sotex/Uni/PRI/TP6/w3.css"/>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <p>{title}</p>
                <form action = "http://172.31.148.23:8000/upload" method = "POST" enctype = "multipart/form-data">
        '''

    for (key,value) in info.items():
        print(value)
        if (value["type"] == "radio"): 
            html += f'''
                        <p>{value["title"]}</p>
                    '''

            for (key2,value2) in value.items():
                if (key2 != "type" and key2 != "title") :
                    html += f'''
                                <input type="radio" id="{value2}" name="{value["title"]}" value="{value2}">
                                <label for="{value["title"]}">{value2}</label>
                            '''

        elif (value["type"] == "select"): 

            html += f'''
                        <p>{value["title"]}</p>
                        <p><select id="{value2}" name="{value["title"]}">
                    '''

            for value2 in value["text"]:
                html += f'''
                            <option value="{value2}">{value2}</option>
                        '''
            
            html += f'''
                        </select></p>
                    '''

        elif (value["type"] == "checkbox"): 
            html += f'''
                        <p>{value["title"]} </p>
                    '''

            for value2 in value["text"]:
                html += f'''
                            <input type="checkbox" id="{value2}" name="{value["title"]}" value="{value2}">
                            <label for="{value2}">{value2}</label>
                        '''

        else:
            html += f'''
                    <p>{value["text"]} </p>
                    <div class="form-group">
                        <input type="{value["type"]}" class="form-control" id="{value["text"]}" name="{value["text"]}">
                    </div>
                    ''' 

    html += f'''
            <p><input type="submit"/></p>
            </form>
            </body>
            </html>
            '''

    return html
