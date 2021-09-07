import unittest

import network_benchmark


class PingTest(unittest.TestCase):

    def testPingNoDNS(self):
        assert network_benchmark.LatencyBenchmark('8.8.8.8') is not None

    def testPingNoDNSCustomTimeout(self):
        assert network_benchmark.LatencyBenchmark('8.8.8.8', 300) is not None

    def testPingDNS(self):
        assert network_benchmark.LatencyBenchmark('google.com') is not None

    def testPingDNSCustomTimeout(self):
        assert network_benchmark.LatencyBenchmark('google.com', 300) is not None

    def testPingWrongDNS(self):
        try:
            assert network_benchmark.LatencyBenchmark('google.cx') is not None
        except IndexError:
            pass
        except Exception as e:
            self.fail('Failed with exception: ', e)

    def testPingWrongNoDNS(self):
        try:
            assert network_benchmark.LatencyBenchmark('256.232.111.0') is not None
        except IndexError:
            pass
        except Exception as e:
            self.fail('Failed with exception: ', e)


if __name__ == '__main__':
    unittest.main()
