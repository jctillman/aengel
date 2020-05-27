
import logging
import time
import sys

from settings import get_settings
from timed import TimedEvent


logging.basicConfig(level="INFO")

def main():
    settings = get_settings(sys.argv[1])
    unlabledEvent = TimedEvent(settings['unlabeled']['timing'], settings['unlabeled']['command'])
    startupEvent = TimedEvent(settings['startup']['timing'], settings['startup']['command'])
    while True:
        unlabledEvent.check()
        startupEvent.check()
        time.sleep(0.25)        