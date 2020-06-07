
import sys

from run.unlabeled.main import main as unlabeled_main
from run.startup.main import main as startup_main
from run.train.main import main as train_main

def go():

    print(sys.argv)
    boot = sys.argv[2]
    if boot == "unlabeled":
        unlabeled_main()
        return

    if boot == "startup":
        startup_main()
        return

    if boot == "train":
        train_main()
        return

if __name__ == "__main__":
    go()

