import os
github_workspace = os.getenv("GITHUB_WORKSPACE")
for root, dirs, files in os.walk(github_workspace):
    for file in files:
        print(os.path.join(root, file))
