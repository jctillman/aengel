
from random import randrange
from subprocess import run
from time import time, localtime


from jsonschema import validate

from lib.timed.schema import schema
from lib.timed.utils import timing_within_interval


class TimedEvent:

    def __init__(self, timing, command):
        validate(instance=timing, schema=schema)
        self.timing = timing
        self.command = command
        self.set_next_time()

    def get_next_interval(self):
        return randrange(self.timing['minimum_interval'], self.timing["maximum_interval"])

    def set_next_time(self):
        self.do_after_time = time() + self.get_next_interval()

    def check(self):
        if (timing_within_interval(self.timing) and self.do_after_time < time()):
            self.set_next_time()
            run(self.command)

