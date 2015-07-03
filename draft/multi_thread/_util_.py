import os
CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))

for i in range(1991, 2011):
    if not os.path.exists(os.path.join(CURRENT_FOLDER, str(i))):
        os.mkdir(os.path.join(CURRENT_FOLDER, str(i)))
