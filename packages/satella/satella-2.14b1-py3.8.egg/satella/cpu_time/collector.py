import typing as tp
import threading
import multiprocessing
import time

import psutil

from satella.coding.structures import Singleton
from satella.coding.transforms import percentile


@Singleton
class CPUProfileBuilderThread(threading.Thread):
    """
    A CPU profile builder thread

    :param window_seconds: the amount of seconds for which to collect data
    :param refresh_each: time of seconds to sleep between rebuilding of profiles
    """
    def __init__(self, window_seconds: int = 300, refresh_each: int = 1800,
                 percentiles_requested: tp.Sequence[float] = (0.9, )):
        super().__init__(name='CPU profile builder', daemon=True)
        self.window_size = window_seconds
        self.refresh_each = refresh_each
        self.data = []
        self.minimum_of = None
        self.maximum_of = None
        self.percentiles_requested = list(percentiles_requested)
        self.percentile_values = []
        self.percentiles_regenerated = False
        self.start()

    def request_percentile(self, percent: float) -> None:
        if percent not in self.percentiles_requested:
            self.percentiles_requested.append(percent)
        self.percentiles_regenerated = False

    def percentile(self, percent: float) -> float:
        if not self.data:
            return 0
        if percent in self.percentiles_requested and self.percentiles_regenerated:
            return self.percentile_values[self.percentiles_requested.index(percent)]
        else:
            return percentile(self.data, percent)

    def is_done(self) -> bool:
        return bool(self.data)

    def recalculate(self) -> None:
        data = []
        calculate_occupancy_factor()    # as first values tend to be a bit wonky
        for _ in range(self.window_size):
            time.sleep(1)
            data.append(calculate_occupancy_factor())
        percentiles = []
        for percent in self.percentiles_requested:
            percentiles.append(percentile(data, percent))
        self.percentile_values = percentiles
        self.percentiles_regenerated = True
        self.minimum_of = min(data)
        self.maximum_of = max(data)
        self.data = data

    def run(self):
        while True:
            time.sleep(self.refresh_each)
            self.recalculate()


def sleep_except(seconds: float, of_below: tp.Optional[float] = None,
                 of_above: tp.Optional[float] = None,
                 check_each: float = 1) -> bool:
    """
    Sleep for specified number of seconds.

    Quit earlier if the occupancy factor goes below of_below or above of_above
    :param seconds:
    :param of_below:
    :param of_above:
    :param check_each: amount of seconds to sleep at once
    :return: whether was awoken due to CPU time condition
    """
    of = calculate_occupancy_factor()
    while seconds > 0:
        if of_above is not None:
            if of_above < of:
                return True
        if of_below is not None:
            if of_below > of:
                return True
        time_to_sleep = min(seconds, check_each)
        time.sleep(time_to_sleep)
        seconds -= time_to_sleep
        if seconds <= 0:
            return False
        of = calculate_occupancy_factor()
    return False


previous_cf: float = None
previous_timestamp: float = None


def _calculate_occupancy_factor() -> float:
    c = psutil.cpu_times()
    try:
        try:
            try:
                used = c.user + c.nice + c.system + c.irq + c.softirq + c.steal + c.guest + c.guest_nice
            except AttributeError:
                # Linux?
                used = c.user + c.nice + c.system + c.irq + c.softirq
        except AttributeError:
            # UNIX ?
            used = c.user + c.nice + c.system
    except AttributeError:
        # windows?
        used = c.user + c.system + c.interrupt
    cur_time = time.monotonic()
    occupation_factor = used / multiprocessing.cpu_count()
    global previous_timestamp, previous_cf
    if previous_timestamp is None:
        previous_cf = occupation_factor
        previous_timestamp = cur_time
        return
    delta = cur_time - previous_timestamp
    if delta == 0:
        return
    of = (occupation_factor - previous_cf)/delta
    previous_cf = occupation_factor
    previous_timestamp = cur_time
    return of


def calculate_occupancy_factor() -> float:
    """
    Return a float between 0 and 1 telling you how occupied is your system.

    Note that this will be the average between now and the time it was last called.

    This in rare cases may block for up to 0.1 seconds
    """
    c = _calculate_occupancy_factor()
    while c is None:
        time.sleep(0.1)
        c = _calculate_occupancy_factor()
    return c


calculate_occupancy_factor()
