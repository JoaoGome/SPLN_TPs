import xml.etree.ElementTree as ET

def parseFile (filePath:str):

    dict = {}
    id = 1
    tree = ET.parse(filePath)

    rootElement = tree.getroot()

    for child in rootElement:
        if (child.tag == "id"):
            dict["id"] = f"{child.text}"

        elif (child.tag == "item"):
            tempDict = {}
            tempDict["type"] = child.attrib["type"]
            for itemChild in child:
                if (itemChild.tag == "text"):
                    tempDict["text"] = f"{itemChild.text}"
            
            dict[f"item{id}"] = tempDict
            id += 1

    return dict