import xml.etree.ElementTree as ET

def parseFile (filePath:str):

    dict = {}
    itemID = 1
    tree = ET.parse(filePath)

    rootElement = tree.getroot()

    for child in rootElement:
        if (child.tag == "id"):
            dict["id"] = f"{child.text}"

        elif (child.tag == "item"):
            tempDict = {}
            textID = 1
            if (child.attrib["type"] == "select"):
                tempDict["type"] = "select"
                for itemChild in child:
                    if (itemChild.tag == "title"):
                        tempDict["title"] = f"{itemChild.text}"
                    elif (itemChild.tag == "text"):
                        tempDict[f"text{textID}"] = f"{itemChild.text}"
                        textID += 1
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
    id = info["id"]
    info.pop("id")

    html = f'''
        <html>
            <body>
                <p>{id}</p>
                <form action = "http://172.31.148.23:8000/upload" method = "POST" enctype = "multipart/form-data">
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

    return html
