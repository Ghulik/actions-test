import os
import xml.etree.ElementTree as ET
from github import Github

github_workspace = os.getenv("GITHUB_WORKSPACE")
key = os.getenv("API_KEY")

g = Github(key)
results = g.search_code('org:Ghulik test')


def getFieldsToRemove():
    tree = ET.parse('destructiveChanges.xml')
    root = tree.getroot()
    foundMatches = []
    for child in root:
        if "types" in child.tag:
            containsCheckedMeta = False
            for secondChild in child:
                if "CustomField" in secondChild.text:
                    containsCheckedMeta = True
            if containsCheckedMeta:
                for secondChild in child:
                    if "members" in secondChild.tag:
                        split_string = secondChild.text.split(".", 1)
                        if(len(split_string) > 1):
                            apiname = split_string[1]
                            foundMatches.append(apiname)
    print('Fields found in destructive changes to be removed: {}'.format(foundMatches))
    return foundMatches

getFieldsToRemove()

for res in results:
    print('Found match.. File: {} Repository: {}" Path:{}'.format(res.name, res.repository.full_name, res.path))
