import os

from github import Github


org:github extension:js test

g = Github("${{secrets.ACCESS_TOKEN}}")

results = g.search_code('search_code')

for res in results:
    print("Found matched results:".format(res.text_matches))
