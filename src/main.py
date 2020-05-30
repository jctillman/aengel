
import logging
import time
import sys

from settings.get_settings import get_settings
from schema import master_schema
from timed import TimedEvent

logging.basicConfig(level="INFO")

def main():
    settings = get_settings(sys.argv[1], master_schema)
    unlabledEvent = TimedEvent(settings['unlabeled']['timing'], settings['unlabeled']['command'])
    startupEvent = TimedEvent(settings['startup']['timing'], settings['startup']['command'])
    while True:
        unlabledEvent.check()
        startupEvent.check()
        time.sleep(0.5)        