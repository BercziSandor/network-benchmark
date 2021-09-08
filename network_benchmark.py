import datetime
import sys
import time
from typing import List

import numpy
from ping3 import ping


# based on: https://github.com/matthieu-lapeyre/network-benchmark

class LatencyBenchmark(object):
    def __init__(self, servers: List[dict], interval_in_sec: float = 1.0, timeout_in_sec: float =
    0.2):
        object.__init__(self)
        if not isinstance(servers, list):
            print("Parameter 'servers' isn't a list, aborting'")
            sys.exit(1)

        self.servers = servers
        self.interval_in_sec = interval_in_sec

        self.timeout_in_sec = timeout_in_sec

        self.test_timestamps = []
        self.network_latency = dict()
        self.network_latency_np = dict()
        self.network_timeout_count = dict()
        self.network_timeout_percent = dict()
        for server in servers:
            alias = server.get("alias")
            self.network_latency[alias] = []
            self.network_latency_np[alias] = []
            self.network_timeout_count[alias]: int = 0
            self.network_timeout_percent[alias]: float = 0.0

    def run_test(self, n_test):
        for n in range(n_test):
            ts = datetime.datetime.now()
            self.test_timestamps.append(ts)
            print(f'Test {n + 1}/{n_test} - {ts}')
            for server in self.servers:
                server_name = server.get('name')
                server_alias = server.get('alias')
                try:
                    ping_time_orig = ping(server_name, timeout=1)
                    if not ping_time_orig or ping_time_orig > self.timeout_in_sec:
                        raise Exception
                    ping_time_ms = round(float(ping_time_orig) * 1000, 0)

                except Exception:
                    ping_time_ms = numpy.nan
                    self.network_timeout_count[server_alias] += 1

                self.network_latency[server_alias].append(ping_time_ms)
                self.network_timeout_percent[server_alias] = \
                    self.network_timeout_count[server_alias] / float(n + 1)
                self.network_latency_np[server_alias] = numpy.array(
                    self.network_latency[server_alias])

                self.get_results(server_alias=server_alias, ping_time_ms=ping_time_ms)

            print(f'Waiting {self.interval_in_sec} seconds...\n')
            time.sleep(self.interval_in_sec)

    def get_results(self, server_alias, ping_time_ms):
        print(' {:<30} {}ms (x̄: {} ({}) ± {} ({}))'.format(
            server_alias + ":", ping_time_ms,
            numpy.nanmean(self.network_latency_np[server_alias]).round(decimals=2),
            numpy.nanmean(self.network_latency_np[server_alias][-3:]).round(decimals=2),
            numpy.nanstd(self.network_latency_np[server_alias]).round(decimals=2),
            numpy.nanstd(self.network_latency_np[server_alias][-3:]).round(decimals=2)
        ))


if __name__ == '__main__':
    servers = list()
    servers = [
        {
            'name': 'tmv2626.devlab.de.tmo',
            'alias': 'build server'
        },
        {
            'name': 'rbe-wbench.workbench.telekom.de',
            'alias': 'workbench'
        },
        {
            'name': 'jira.devops.telekom.de',
            'alias': 'Jira'
        },
        {
            'name': 'qdehxd.de.t-internal.com',
            'alias': 'RBE ABN APP'
        },
        {
            'name': 'qdehxe.de.t-internal.com',
            'alias': 'RBE ABN API'
        },
        {
            'name': 'qderxx.de.t-internal.com',
            'alias': 'RBE P3 API'
        },
        {
            'name': 'qderxy.de.t-internal.com',
            'alias': 'RBE P3 APP'
        },
        {
            'name': 'tmv2331.devlab.de.tmo',
            'alias': 'RBE Preint APP'
        },
        {
            'name': 'QDEC2N.de.t-internal.com',
            'alias': 'RPM Repo'
        },
        {
            'name': 'telekom.sharepoint.de',
            'alias': 'Sharepoint'
        },

    ]

    test = LatencyBenchmark(servers=servers, interval_in_sec=2)
    test.run_test(50)
