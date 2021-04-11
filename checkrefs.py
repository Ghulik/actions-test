import os

from github import Github
github_workspace = os.getenv("GITHUB_WORKSPACE")
key = os.getenv("API_KEY")

g = Github(key)
results = g.search_code('org:Ghulik test')

for res in results:
    print('Found match.. File: {} Repository: {}" Path:{}'.format(res.name, res.repository.full_name, res.path))
