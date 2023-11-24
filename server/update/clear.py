import os

path = '/update/'
def clear():
    for i in os.listdir(path):
        if i.endswith('.xlsx') or i.endswith('.crdownload'):
            os.remove(path+i)
clear()
