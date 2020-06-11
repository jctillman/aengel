
import sys

from run.unlabeled.main import main as unlabeled_main
from run.startup.main import main as startup_main
from run.train.main import main as train_main

#
# Run when wishing to start
# some secondary task.  Started
# often by main loop from 'main.py',
# see the default.json for example of commands.
# 

def go():

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

