import os

from github import Github


#org:github extension:js test

g = Github("${{ process.env.API_KEY }}")

results = g.search_code('search_code')

for res in results:
    print("Found matched results:".format(res.text_matches))
