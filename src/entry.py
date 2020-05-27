
import sys

from main import main
from unlabeled.main import main as unlabeled_main
from startup.main import main as startup_main

def go():

    if len(sys.argv) < 3:
        main()
        return

    boot = sys.argv[2]
    if boot == "unlabeled":
        unlabeled_main()
        return

    if boot == "startup":
        startup_main()
        return

if __name__ == "__main__":
    go()

