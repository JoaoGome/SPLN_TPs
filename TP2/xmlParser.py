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