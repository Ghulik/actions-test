import os

from github import Github
key = os.getenv("API_KEY")
print("key " + key)
#org:github extension:js test

g = Github(key)
results = g.search_code('search_code')

for res in results:
    print("Found matched results:".format(res.text_matches))
