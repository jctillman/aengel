import time
import sys

from lib.settings.get_settings import get_settings
from lib.timed import TimedEvent

from run.loop.schema import schema

def main():
    settings = get_settings(sys.argv[1], schema)
    unlabled_event = TimedEvent(settings['unlabeled']['timing'], settings['unlabeled']['command'])
    startup_event = TimedEvent(settings['startup']['timing'], settings['startup']['command'])
    while True:
        unlabled_event.check()
        startup_event.check()
        time.sleep(0.333)        