import os
import xml.etree.ElementTree as ET
from github import Github

github_workspace = os.getenv("GITHUB_WORKSPACE")
key = os.getenv("API_KEY")
prid = os.getenv("PR_NUMBER")
repo_name = "Ghulik/actions-test"

# Search for CustomFields referenced in desctructiveChanges.xml
def getFieldsToRemove():
    foundMatches = []
    try:
        tree = ET.parse('destructiveChanges.xml')
        root = tree.getroot()
        
        for child in root:
            if "types" in child.tag:
                containsCheckedMeta = False
                for secondChild in child:
                    if "CustomField" in secondChild.text:
                        containsCheckedMeta = True
                if containsCheckedMeta is True:
                    for secondChild in child:
                        if "members" in secondChild.tag:
                            split_string = secondChild.text.split(".", 1)
                            if(len(split_string) > 1):
                                apiname = split_string[1]
                                foundMatches.append(apiname)
        print('Fields found in destructive changes to are going to be removed from salesforce: {}'.format(foundMatches))
    except FileNotFoundError:
        # Destruction changes file not found, exit success
        print('destructiveChanges.xml not found')
        exit(0)
    return foundMatches

fieldToCheck = getFieldsToRemove()

# destructionChange.xml did not contain any CustomFields
if(len(fieldToCheck) == 0):
    print('destructiveChanges.xml does not contain CustomField type')
    exit(0)  
    
# Search github for refences in code
g = Github(key)

# Vars for output comment
outputTable = "**Found these references:**\n\n| Search Term | Path | Repository |\n| :--- | :--- | :--- |\n"
tableColumDelimiter = "|"
newLine = "\n"
tableRows = ""
backTick = "`"
for searchTerm in fieldToCheck:
    results = g.search_code('org:Ghulik ' + searchTerm)
    for res in results:
        # Ignore base repo
        if res.repository.full_name not in repo_name
            repoName = res.repository.full_name
            repoPath = res.path
            tableRows += tableColumDelimiter + backTick + searchTerm + backTick + tableColumDelimiter + repoPath + tableColumDelimiter + repoName + tableColumDelimiter + newLine
            print('Found match.. File: {} Repository: {}" Path:{}'.format(res.name, res.repository.full_name, res.path))
outputTable += tableRows

if not prid:
    # Can happen when running action manually, then we will not be commenting any PR
    print("Missing PR")
else:
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(prid))
    pr.create_issue_comment(outputTable)
    
