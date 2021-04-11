import os
for root, dirs, files in os.walk("${{env.working-directory}}"):
    for file in files:
        print(os.path.join(root, file))
