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

            tempDict["required"] = False
            if "required" in child.attrib:
                if child.attrib["required"].lower() == "true":
                    tempDict["required"] = True

            if (child.attrib["type"].lower() == "radio"):
                tempDict["type"] = "radio"
                tempDict["text"] = []
                for itemChild in child:
                    if (itemChild.tag.lower() == "title"):
                        tempDict["title"] = f"{itemChild.text}"
                    elif (itemChild.tag.lower() == "text"):
                        tempDict[f"text"].append(f"{itemChild.text}")
                dict[f"item{itemID}"] = tempDict
                itemID += 1

            elif (child.attrib["type"].lower() == "checkbox"):
                tempDict["type"] = "checkbox"
                tempDict["text"] = []
                for itemChild in child:
                    if (itemChild.tag.lower() == "title"):
                        tempDict["title"] = f"{itemChild.text}"
                    elif (itemChild.tag.lower() == "text"):
                        tempDict[f"text"].append(f"{itemChild.text}")
                dict[f"item{itemID}"] = tempDict
                itemID += 1

            elif (child.attrib["type"].lower() == "select"):
                tempDict["type"] = "select"
                tempDict["text"] = []
                for itemChild in child:
                    if (itemChild.tag.lower() == "title"):
                        tempDict["title"] = f"{itemChild.text}"
                    elif (itemChild.tag.lower() == "text"):
                        tempDict[f"text"].append(f"{itemChild.text}")
                dict[f"item{itemID}"] = tempDict
                itemID += 1

            else:
                tempDict["type"] = child.attrib["type"]
                for itemChild in child:
                    if (itemChild.tag.lower() == "text"):
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
                <link rel="stylesheet" href="static/styles/w3.css"/>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            </head>
            <body>
                <h3 class="w3-cyan w3-center w3-margin w3-text-white"><b>{title}</b></h3>
                <form class="w3-container w3-left-margin" action = "http://172.31.148.23:8000/upload" method = "POST" enctype = "multipart/form-data">
        '''

    for (key,value) in info.items():
        if value["required"] == True: is_required = "required"
        else: is_required = ""

        if (value["type"] == "radio"): 
            html += f'''
                        <label class="w3-text-blue-grey"><b>{value["title"]}:</b></label>
                    '''

            for value2 in value["text"]:
                html += f'''
                            <input type="radio" id="{value2}" name="{value["title"]}" value="{value2}" {is_required}>
                            <label for="{value["title"]}">{value2}</label>
                        '''
            html += '<br/><br/>'

        elif (value["type"] == "select"): 

            html += f'''
                        <label class="w3-text-blue-grey"><b>{value["title"]}:</b></label>
                        <select id="{value2}" name="{value["title"]}" {is_required}>
                    '''

            for value2 in value["text"]:
                html += f'''
                            <option value="{value2}">{value2}</option>
                        '''
            
            html += f'''
                        </select><br/><br/>
                    '''

        elif (value["type"] == "checkbox"): 
            html += f'''
                        <label class="w3-text-blue-grey"><b>{value["title"]}:</b></label>
                    '''

            for value2 in value["text"]:
                html += f'''
                            <input type="checkbox" id="{value2}" name="{value["title"]}" value="{value2}" {is_required}>
                            <label for="{value2}">{value2}</label>
                        '''
            html += '<br/><br/>'

        else:
            html += f'''
                    <label class="w3-text-blue-grey"><b>{value["text"]}:</b></label>
                    <input type="{value["type"]}" class="form-control" id="{value["text"]}" name="{value["text"]}" {is_required}><br/><br/>
                    ''' 

    html += f'''
            <p class="w3-cyan"><b><input class="w3-button w3-text-white w3-round" type="submit"/></b></p>
            </form>
            <br class="w3-pale-blue"/>
            </body>
            </html>
            '''

    return html
