
import sys
import os
import glob
import json

from main import main
from unlabeled.main import main as unlabeled_main
from startup.main import main as startup_main
from train.main import main as train_main

def go():
    jsons = glob.glob('./data/labeled/*.json')
    pngs = glob.glob('./data/labeled/*.png')
    jsons.sort()
    pngs.sort()

    for i, js in enumerate(jsons):
        json_file = open(js)
        data = json.load(json_file)
        if (data["answers"][0] == "absent"):
            print(data["answers"])
            os.remove(pngs[i])
            os.remove(jsons[i])

if __name__ == "__main__":
    go()

