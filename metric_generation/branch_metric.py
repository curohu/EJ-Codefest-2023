from random import randint
from datetime import datetime


class BranchMetric:

    def __init__(self, branch_name, spike_threshold, first_timestamp=0, period=86400, increment=60):
        self.branch_name = branch_name
        self.first_timestamp = first_timestamp
        self.metric_array = {self.first_timestamp: randint(15, 35)}
        self.last_timestamp = self.first_timestamp
        self.spike_value = 0
        self.spike_threshold = spike_threshold
        self.period = period
        self.increment = increment

    def __str__(self):
        return f"{self.branch_name}"

    def generate_metric(self, spike_modifier):
        self.last_timestamp = self.get_last_timestamp()
        last_metric = self.metric_array[self.last_timestamp]
        if spike_modifier == 0:
            if last_metric >= 35:
                return last_metric + randint(-10, 1)
            elif last_metric <= 15:
                return last_metric + randint(0, 2)
            return last_metric + randint(-2, 2)
        elif spike_modifier > 0:
            if last_metric < 100:
                return self.get_metric_by_timestamp(self.last_timestamp) + randint(0, spike_modifier)
            else:
                return 100

    def get_metric_by_timestamp(self, metric_timestamp):
        return self.metric_array[metric_timestamp]

    def set_metric(self, metric, metric_timestamp=int(datetime.now().timestamp())):
        self.metric_array[metric_timestamp] = metric

    def get_last_timestamp(self):
        return max(self.metric_array.keys())

    def is_spiking(self):
        return self.spike_value > 1000 - (10 * self.spike_threshold)

    def update_spike_value(self):
        if self.is_spiking():
            self.spike_value = (self.spike_value + randint(0, 1)) % 1000
        else:
            self.spike_value = (self.spike_value + randint(-5, 15)) % 1000

    def create_metric_array(self):
        for ts in range(self.first_timestamp, self.first_timestamp + self.period, self.increment):
            spike_modifier = self.spike_value % 10 if self.is_spiking() else 0
            current_metric = self.generate_metric(spike_modifier)
            self.set_metric(current_metric, ts)
            self.update_spike_value()

    def get_metric_array(self):
        self.metric_array["Branch Name"] = self.branch_name
        return self.metric_array
